from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models.bill import Bill
from mysql_connector import db

bill_bp = Blueprint('bill', __name__, url_prefix='/bills')

@bill_bp.route('', methods=['GET'])
@login_required
def get_bills():
    bills = Bill.query.filter_by(user_id=current_user.id).all()
    return jsonify([bill.to_dict() for bill in bills])

@bill_bp.route('/<int:id>', methods=['GET'])
@login_required
def get_bill(id):
    bill = Bill.query.get_or_404(id)
    if bill.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 403
    return jsonify(bill.to_dict())

@bill_bp.route('', methods=['POST'])
@login_required
def create_bill():
    data = request.get_json()
    bill = Bill(
        user_id=current_user.id,
        biller_name=data['biller_name'],
        due_date=data['due_date'],
        amount=data['amount'],
        account_id=data['account_id']
    )
    db.session.add(bill)
    db.session.commit()
    return jsonify({'message': 'Bill created successfully'}), 201

@bill_bp.route('/<int:id>', methods=['PUT'])
@login_required
def update_bill(id):
    bill = Bill.query.get_or_404(id)
    if bill.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 403

    data = request.get_json()
    bill.biller_name = data.get('biller_name', bill.biller_name)
    bill.due_date = data.get('due_date', bill.due_date)
    bill.amount = data.get('amount', bill.amount)
    bill.account_id = data.get('account_id', bill.account_id)
    db.session.commit()
    return jsonify({'message': 'Bill updated successfully'})

@bill_bp.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_bill(id):
    bill = Bill.query.get_or_404(id)
    if bill.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 403
    db.session.delete(bill)
    db.session.commit()
    return jsonify({'message': 'Bill deleted successfully'})
