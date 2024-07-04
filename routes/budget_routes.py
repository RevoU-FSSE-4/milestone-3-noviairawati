from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models.budget import Budget
from mysql_connector import db

budget_bp = Blueprint('budget', __name__, url_prefix='/budgets')

@budget_bp.route('', methods=['GET'])
@login_required
def get_budgets():
    budgets = Budget.query.filter_by(user_id=current_user.id).all()
    return jsonify([budget.to_dict() for budget in budgets])

@budget_bp.route('/<int:id>', methods=['GET'])
@login_required
def get_budget(id):
    budget = Budget.query.get_or_404(id)
    if budget.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 403
    return jsonify(budget.to_dict())

@budget_bp.route('', methods=['POST'])
@login_required
def create_budget():
    data = request.get_json()
    budget = Budget(
        user_id=current_user.id,
        name=data['name'],
        amount=data['amount'],
        start_date=data['start_date'],
        end_date=data['end_date']
    )
    db.session.add(budget)
    db.session.commit()
    return jsonify({'message': 'Budget created successfully'}), 201

@budget_bp.route('/<int:id>', methods=['PUT'])
@login_required
def update_budget(id):
    budget = Budget.query.get_or_404(id)
    if budget.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 403

    data = request.get_json()
    budget.name = data.get('name', budget.name)
    budget.amount = data.get('amount', budget.amount)
    budget.start_date = data.get('start_date', budget.start_date)
    budget.end_date = data.get('end_date', budget.end_date)
    db.session.commit()
    return jsonify({'message': 'Budget updated successfully'})

@budget_bp.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_budget(id):
    budget = Budget.query.get_or_404(id)
    if budget.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 403
    db.session.delete(budget)
    db.session.commit()
    return jsonify({'message': 'Budget deleted successfully'})
