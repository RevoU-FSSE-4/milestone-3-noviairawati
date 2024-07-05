from flask import Blueprint, request, jsonify
from ..models.budget import Budget
from ..mysql_connector import db
from flask_login import login_required, current_user

bp = Blueprint("budget_routes", __name__, url_prefix="/budgets")


@bp.route("", methods=["POST"])
@login_required
def create_budget():
    data = request.json
    name = data["name"]
    amount = data["amount"]
    start_date = data["start_date"]
    end_date = data["end_date"]

    budget = Budget(
        user_id=current_user.id,
        name=name,
        amount=amount,
        start_date=start_date,
        end_date=end_date,
    )

    db.session.add(budget)
    db.session.commit()

    return jsonify({"message": "Budget created successfully"}), 201


@bp.route("", methods=["GET"])
@login_required
def get_budgets():
    budgets = Budget.query.filter_by(user_id=current_user.id).all()
    return (
        jsonify(
            [
                {
                    "id": budget.id,
                    "name": budget.name,
                    "amount": budget.amount,
                    "start_date": budget.start_date,
                    "end_date": budget.end_date,
                }
                for budget in budgets
            ]
        ),
        200,
    )


@bp.route("/<int:id>", methods=["PUT"])
@login_required
def update_budget(id):
    budget = Budget.query.filter_by(id=id, user_id=current_user.id).first()
    if not budget:
        return jsonify({"error": "Budget not found"}), 404

    data = request.json
    budget.name = data.get("name", budget.name)
    budget.amount = data.get("amount", budget.amount)
    budget.start_date = data.get("start_date", budget.start_date)
    budget.end_date = data.get("end_date", budget.end_date)

    db.session.commit()
    return jsonify({"message": "Budget updated successfully"}), 200
