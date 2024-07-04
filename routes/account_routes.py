from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models.account import Account
from mysql_connector import db

account_bp = Blueprint('account', __name__, url_prefix='/accounts')

@account_bp.route('', methods=['GET'])
@login_required
def get_accounts():
    accounts = Account.query.filter_by(user_id=current_user.id).all()
    return jsonify([account.to_dict() for account in accounts])

@account_bp.route('/<int:id>', methods=['GET'])
@login_required
def get_account(id):
    account = Account.query.get_or_404(id)
    if account.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 403
    return jsonify(account.to_dict())

@account_bp.route('', methods=['POST'])
@login_required
def create_account():
    data = request.get_json()
    account = Account(
        user_id=current_user.id,
        account_type=data['account_type'],
        account_number=data['account_number'],
        balance=data['balance']
    )
    db.session.add(account)
    db.session.commit()
    return jsonify({'message': 'Account created successfully'}), 201

@account_bp.route('/<int:id>', methods=['PUT'])
@login_required
def update_account(id):
    account = Account.query.get_or_404(id)
    if account.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 403

    data = request.get_json()
    account.account_type = data.get('account_type', account.account_type)
    account.account_number = data.get('account_number', account.account_number)
    account.balance = data.get('balance', account.balance)
    db.session.commit()
    return jsonify({'message': 'Account updated successfully'})

@account_bp.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_account(id):
    account = Account.query.get_or_404(id)
    if account.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 403
    db.session.delete(account)
    db.session.commit()
    return jsonify({'message': 'Account deleted successfully'})
