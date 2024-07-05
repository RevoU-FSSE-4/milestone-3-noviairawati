from flask import Blueprint, request, jsonify
from ..models.account import Account
from ..mysql_connector import db
from flask_login import login_required, current_user

bp = Blueprint("account_routes", __name__, url_prefix="/accounts")


@bp.route("", methods=["POST"])
@login_required
def create_account():
    data = request.json
    account_type = data["account_type"]
    account_number = data["account_number"]
    balance = data["balance"]

    account = Account(
        user_id=current_user.id,
        account_type=account_type,
        account_number=account_number,
        balance=balance,
    )

    db.session.add(account)
    db.session.commit()

    return jsonify({"message": "Account created successfully"}), 201


@bp.route("", methods=["GET"])
@login_required
def get_accounts():
    accounts = Account.query.filter_by(user_id=current_user.id).all()
    return (
        jsonify(
            [
                {
                    "id": account.id,
                    "account_type": account.account_type,
                    "account_number": account.account_number,
                    "balance": account.balance,
                    "created_at": account.created_at,
                    "updated_at": account.updated_at,
                }
                for account in accounts
            ]
        ),
        200,
    )


@bp.route("/<int:id>", methods=["GET"])
@login_required
def get_account(id):
    account = Account.query.filter_by(id=id, user_id=current_user.id).first()
    if not account:
        return jsonify({"error": "Account not found"}), 404
    return (
        jsonify(
            {
                "id": account.id,
                "account_type": account.account_type,
                "account_number": account.account_number,
                "balance": account.balance,
                "created_at": account.created_at,
                "updated_at": account.updated_at,
            }
        ),
        200,
    )


@bp.route("/<int:id>", methods=["PUT"])
@login_required
def update_account(id):
    account = Account.query.filter_by(id=id, user_id=current_user.id).first()
    if not account:
        return jsonify({"error": "Account not found"}), 404

    data = request.json
    account.account_type = data.get("account_type", account.account_type)
    account.account_number = data.get("account_number", account.account_number)
    account.balance = data.get("balance", account.balance)

    db.session.commit()
    return jsonify({"message": "Account updated successfully"}), 200


@bp.route("/<int:id>", methods=["DELETE"])
@login_required
def delete_account(id):
    account = Account.query.filter_by(id=id, user_id=current_user.id).first()
    if not account:
        return jsonify({"error": "Account not found"}), 404

    db.session.delete(account)
    db.session.commit()
    return jsonify({"message": "Account deleted successfully"}), 200
