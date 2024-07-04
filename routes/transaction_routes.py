from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models.transaction import Transaction
from models.account import Account
from mysql_connector import db

transaction_bp = Blueprint('transaction', __name__, url_prefix='/transactions')

@transaction_bp.route('', methods=['GET'])
@login_required
def get_transactions():
    accounts = Account.query.filter_by(user_id=current_user.id).all()
    account_ids = [account.id for account in accounts]
    transactions = Transaction.query.filter(
        (Transaction.from_account_id.in_(account_ids)) |
        (Transaction.to_account_id.in_(account_ids))
    ).all()
    return jsonify([transaction.to_dict() for transaction in transactions])

@transaction_bp.route('/<int:id>', methods=['GET'])
@login_required
def get_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    accounts = Account.query.filter_by(user_id=current_user.id).all()
    account_ids = [account.id for account in accounts]
    
    if transaction.from_account_id not in account_ids and transaction.to_account_id not in account_ids:
        return jsonify({'message': 'Unauthorized'}), 403
    return jsonify(transaction.to_dict())

@transaction_bp.route('', methods=['POST'])
@login_required
def create_transaction():
    data = request.get_json()
    from_account = Account.query.get(data['from_account_id'])
    to_account = Account.query.get(data['to_account_id'])
    
    if from_account.user_id != current_user.id and to_account.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 403

    transaction = Transaction(
        from_account_id=data['from_account_id'],
        to_account_id=data['to_account_id'],
        amount=data['amount'],
        type=data['type'],
        description=data.get('description')
    )
    db.session.add(transaction)
    db.session.commit()
    return jsonify({'message': 'Transaction created successfully'}), 201

@transaction_bp.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    accounts = Account.query.filter_by(user_id=current_user.id).all()
    account_ids = [account.id for account in accounts]
    
    if transaction.from_account_id not in account_ids and transaction.to_account_id not in account_ids:
        return jsonify({'message': 'Unauthorized'}), 403
    
    db.session.delete(transaction)
    db.session.commit()
    return jsonify({'message': 'Transaction deleted successfully'})
