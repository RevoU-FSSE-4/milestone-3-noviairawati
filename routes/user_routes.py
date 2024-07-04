from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from models.user import User
from mysql_connector import db
from werkzeug.security import generate_password_hash, check_password_hash

user_bp = Blueprint('user', __name__, url_prefix='/users')

@user_bp.route('', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({'message': 'User already exists'}), 400
    
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User created successfully'}), 201

@user_bp.route('/me', methods=['GET'])
@login_required
def get_current_user():
    return jsonify({
        'id': current_user.id,
        'username': current_user.username,
        'email': current_user.email
    })

@user_bp.route('/me', methods=['PUT'])
@login_required
def update_current_user():
    data = request.get_json()
    current_user.username = data.get('username', current_user.username)
    current_user.email = data.get('email', current_user.email)
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

@user_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user is None or not user.check_password(password):
            return jsonify({'message': 'Invalid credentials'}), 401
        
        login_user(user)
        return jsonify({'message': 'Logged in successfully'})
    except Exception as e:
        # Log the exception (print to console or use a logging framework)
        print(f"An error occurred during login: {e}")
        return jsonify({'message': 'Login Failed'}), 500


@user_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'})
