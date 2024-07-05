from flask import Blueprint, jsonify
from ..models.transaction import Transaction
from ..mysql_connector import db
from flask_login import login_required
from flask_login import login_required, current_user

bp = Blueprint("transaction_routes", __name__, url_prefix="/transactions")

@bp.route("", methods=["GET"])
@login_required
def get_transactions():
    try:
        transactions = Transaction.query.filter(
            (Transaction.from_account.has(user_id=current_user.id)) |
            (Transaction.to_account.has(user_id=current_user.id))
        ).all()

        if not transactions:
            return jsonify({"message": "No transactions found"}), 404

        transaction_list = []
        for transaction in transactions:
            transaction_data = {
                "id": transaction.id,
                "from_account_id": transaction.from_account_id,
                "to_account_id": transaction.to_account_id,
                "amount": str(transaction.amount),
                "type": transaction.type,
                "description": transaction.description,
                "created_at": transaction.created_at.strftime("%Y-%m-%d %H:%M:%S")
            }
            transaction_list.append(transaction_data)

        return jsonify(transaction_list), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Failed to fetch transactions"}), 500

@bp.route("/<int:id>", methods=["GET"])
@login_required
def get_transaction_by_id(id):
    try:
        transaction = Transaction.query.filter_by(id=id).first()

        if not transaction:
            return jsonify({"error": "Transaction not found"}), 404

        transaction_data = {
            "id": transaction.id,
            "from_account_id": transaction.from_account_id,
            "to_account_id": transaction.to_account_id,
            "amount": str(transaction.amount),
            "type": transaction.type,
            "description": transaction.description,
            "created_at": transaction.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }

        return jsonify(transaction_data), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Failed to fetch transaction"}), 500
