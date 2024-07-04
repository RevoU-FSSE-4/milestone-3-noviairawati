from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from mysql_connector import db

def create_user(username, email, password):
    password_hash = generate_password_hash(password)
    user = User(username=username, email=email, password_hash=password_hash)
    db.session.add(user)
    db.session.commit()
    return user

def authenticate_user(email, password):
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password_hash, password):
        return user
    return None
