from flask import Blueprint, request, jsonify
from ..models.transaction import Transaction
from ..models.account import Account
from ..mysql_connector import db
from flask_login import login_required, current_user

bp = Blueprint('transaction_routes', __name__, url_prefix='/transactions')

@bp.route('', methods=['POST'])
@login_required
def create_transaction():
    data = request.json
    from_account_id = data.get('from_account_id')
    to_account_id = data['to_account_id']
    amount = data['amount']
    type = data['type']
    description = data.get('description')

    if from_account_id:
        from_account = Account.query.filter_by(id=from_account_id, user_id=current_user.id).first()
        if not from_account:
            return jsonify({'error': 'From account not found'}), 404
        from_account.balance -= amount

    to_account = Account.query.filter_by(id=to_account_id, user_id=current_user.id).first()
    if not to_account:
        return jsonify({'error': 'To account not found'}), 404
    to_account.balance += amount

    transaction = Transaction(from_account_id=from_account_id, to_account_id=to_account_id, amount=amount, type=type, description=description)

    db.session.add(transaction)
    db.session.commit()

    return jsonify({'message': 'Transaction created successfully'}), 201

@bp.route('', methods=['GET'])
@login_required
def get_transactions():
    accounts = [account.id for account in current_user.accounts]
    transactions = Transaction.query.filter((Transaction.from_account_id.in_(accounts)) | (Transaction.to_account_id.in_(accounts))).all()
    return jsonify([{
        'id': transaction.id,
        'from_account_id': transaction.from_account_id,
        'to_account_id': transaction.to_account_id,
        'amount': transaction.amount,
        'type': transaction.type,
        'description': transaction.description,
        'created_at': transaction.created_at
    } for transaction in transactions]), 200

@bp.route('/<int:id>', methods=['GET'])
@login_required
def get_transaction(id):
    transaction = Transaction.query.get(id)
    if not transaction or (transaction.from_account.user_id != current_user.id and transaction.to_account.user_id != current_user.id):
        return jsonify({'error': 'Transaction not found'}), 404
    return jsonify({
        'id': transaction.id,
        'from_account_id': transaction.from_account_id,
        'to_account_id': transaction.to_account_id,
        'amount': transaction.amount,
        'type': transaction.type,
        'description': transaction.description,
        'created_at': transaction.created_at
    }), 200
