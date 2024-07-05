from flask import Blueprint, request, jsonify
from ..models.bill import Bill
from ..mysql_connector import db
from flask_login import login_required, current_user

bp = Blueprint("bill_routes", __name__, url_prefix="/bills")


@bp.route("", methods=["POST"])
@login_required
def create_bill():
    data = request.json
    biller_name = data["biller_name"]
    due_date = data["due_date"]
    amount = data["amount"]
    account_id = data["account_id"]

    bill = Bill(
        user_id=current_user.id,
        biller_name=biller_name,
        due_date=due_date,
        amount=amount,
        account_id=account_id,
    )

    db.session.add(bill)
    db.session.commit()

    return jsonify({"message": "Bill created successfully"}), 201


@bp.route("", methods=["GET"])
@login_required
def get_bills():
    bills = Bill.query.filter_by(user_id=current_user.id).all()
    return (
        jsonify(
            [
                {
                    "id": bill.id,
                    "biller_name": bill.biller_name,
                    "due_date": bill.due_date,
                    "amount": bill.amount,
                    "account_id": bill.account_id,
                }
                for bill in bills
            ]
        ),
        200,
    )


@bp.route("/<int:id>", methods=["PUT"])
@login_required
def update_bill(id):
    bill = Bill.query.filter_by(id=id, user_id=current_user.id).first()
    if not bill:
        return jsonify({"error": "Bill not found"}), 404

    data = request.json
    bill.biller_name = data.get("biller_name", bill.biller_name)
    bill.due_date = data.get("due_date", bill.due_date)
    bill.amount = data.get("amount", bill.amount)
    bill.account_id = data.get("account_id", bill.account_id)

    db.session.commit()
    return jsonify({"message": "Bill updated successfully"}), 200


@bp.route("/<int:id>", methods=["DELETE"])
@login_required
def delete_bill(id):
    bill = Bill.query.filter_by(id=id, user_id=current_user.id).first()
    if not bill:
        return jsonify({"error": "Bill not found"}), 404

    db.session.delete(bill)
    db.session.commit()
    return jsonify({"message": "Bill deleted successfully"}), 200
