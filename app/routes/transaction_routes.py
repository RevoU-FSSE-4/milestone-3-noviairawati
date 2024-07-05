from flask import Blueprint, request, jsonify
from ..models.transaction import Transaction
from ..models.account import Account
from ..mysql_connector import db
from flask_login import login_required, current_user
from decimal import Decimal
from sqlalchemy import or_

bp = Blueprint("transaction_routes", __name__, url_prefix="/transactions")


# Retrieve a list of all transactions for the currently authenticated user's accounts
@bp.route("", methods=["GET"])
@login_required
def get_transactions():
    account_id = request.args.get("account_id")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    query = Transaction.query.filter_by(user_id=current_user.id)

    if account_id:
        query = query.filter(
            or_(
                Transaction.from_account_id == account_id,
                Transaction.to_account_id == account_id,
            )
        )

    if start_date:
        query = query.filter(Transaction.timestamp >= start_date)

    if end_date:
        query = query.filter(Transaction.timestamp <= end_date)

    transactions = query.all()

    return jsonify([transaction.serialize() for transaction in transactions]), 200


# Retrieve details of a specific transaction by its ID
@bp.route("/<int:id>", methods=["GET"])
@login_required
def get_transaction(id):
    transaction = Transaction.query.get(id)
    if not transaction:
        return jsonify({"error": "Transaction not found"}), 404

    # Check authorization
    if (
        transaction.from_account.user_id != current_user.id
        and transaction.to_account.user_id != current_user.id
    ):
        return jsonify({"error": "Unauthorized to view this transaction"}), 403

    return jsonify(transaction.serialize()), 200


# Initiate a new transaction (deposit, withdrawal, or transfer)
@bp.route("", methods=["POST"])
@login_required
def create_transaction():
    data = request.json
    from_account_id = data.get("from_account_id")
    to_account_id = data["to_account_id"]
    amount = Decimal(data["amount"])  # Convert amount to Decimal
    type = data["type"]
    description = data.get("description")

    try:
        # Check if from_account_id is provided and valid
        if from_account_id:
            from_account = Account.query.filter_by(
                id=from_account_id, user_id=current_user.id
            ).first()
            if not from_account:
                return jsonify({"error": "From account not found"}), 404
            if from_account.balance < amount:
                return jsonify({"error": "Insufficient balance"}), 400
            from_account.balance -= amount  # Use -= operation with Decimal

        # Find the to_account based on to_account_id
        to_account = Account.query.filter_by(id=to_account_id).first()
        if not to_account:
            return jsonify({"error": "To account not found"}), 404
        if from_account_id and to_account_id == from_account_id:
            return jsonify({"error": "Cannot transfer to the same account"}), 400
        if to_account.user_id != current_user.id:
            return (
                jsonify(
                    {"error": "Unauthorized to perform transaction to this account"}
                ),
                403,
            )
        to_account.balance += amount  # Use += operation with Decimal

        # Create the transaction object
        transaction = Transaction(
            from_account_id=from_account_id,
            to_account_id=to_account_id,
            amount=amount,
            type=type,
            description=description,
            user_id=current_user.id,
        )

        # Add and commit the transaction to the database
        db.session.add(transaction)
        db.session.commit()

        return jsonify({"message": "Transaction created successfully"}), 201

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Failed to create transaction"}), 500
