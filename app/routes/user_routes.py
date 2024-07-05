from flask import Blueprint, request, jsonify
from ..models.user import User
from ..mysql_connector import db
from ..utils.auth import authenticate_user, login_required
from flask_login import login_user, logout_user, current_user

bp = Blueprint("user_routes", __name__, url_prefix="/users")


# Create User
@bp.route("", methods=["POST"])
def create_user():
    try:
        data = request.json
        username = data["username"]
        email = data["email"]
        password = data["password"]

        user = User(username=username, email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        # Log the error (you can use logging library)
        print(f"Error: {e}")
        return jsonify({"error": "Failed Create User"}), 500


@bp.route("/me", methods=["GET"])
@login_required
def get_user():
    try:
        user = current_user
        return (
            jsonify(
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "created_at": user.created_at,
                    "updated_at": user.updated_at,
                }
            ),
            200,
        )
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Failed Login"}), 500


# Update User
@bp.route("/me", methods=["PUT"])
@login_required
def update_user():
    try:
        user = current_user
        data = request.json
        user.username = data.get("username", user.username)
        user.email = data.get("email", user.email)
        if data.get("password"):
            user.set_password(data["password"])
        db.session.commit()
        return jsonify({"message": "User updated successfully"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Failed User Updated"}), 500


# Login User
@bp.route("/login", methods=["POST"])
def login():
    try:
        return authenticate_user()
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Failed Login"}), 500


# Logout User
@bp.route("/logout", methods=["POST"])
@login_required
def logout():
    try:
        logout_user()
        return jsonify({"message": "Logged out successfully"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Failed Logout"}), 500
