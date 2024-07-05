from flask import Blueprint, request, jsonify
from ..models.transaction import Transaction
from ..models.account import Account
from ..mysql_connector import db
from flask_login import login_required, current_user
from decimal import Decimal

bp = Blueprint('transaction_routes', __name__, url_prefix='/transactions')

@bp.route('', methods=['POST'])
@login_required
def create_transaction():
    data = request.json
    from_account_id = data.get('from_account_id')
    to_account_id = data['to_account_id']
    amount = Decimal(data['amount'])
    transaction_type = data['type']
    description = data.get('description')

    try:
        # Check if from_account_id is provided and valid
        if from_account_id:
            from_account = Account.query.filter_by(id=from_account_id, user_id=current_user.id).first()
            if not from_account:
                return jsonify({'error': 'From account not found'}), 404
            if from_account.balance < amount:
                return jsonify({'error': 'Insufficient balance'}), 400
            from_account.balance -= amount

        # Find the to_account based on to_account_id
        to_account = Account.query.filter_by(id=to_account_id).first()
        if not to_account:
            return jsonify({'error': 'To account not found'}), 404
        if from_account_id and to_account_id == from_account_id:
            return jsonify({'error': 'Cannot transfer to the same account'}), 400
        if to_account.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized to perform transaction to this account'}), 403
        to_account.balance += amount

        # Create the transaction object with user_id
        transaction = Transaction(
            from_account_id=from_account_id,
            to_account_id=to_account_id,
            amount=amount,
            type=transaction_type,
            description=description,
            user_id=current_user.id  # Ensure user_id is passed correctly
        )

        # Add and commit the transaction to the database
        db.session.add(transaction)
        db.session.commit()

        return jsonify({'message': 'Transaction created successfully'}), 201

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Failed to create transaction"}), 500
