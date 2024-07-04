from models.user import User
from mysql_connector import db

def get_user_by_id(user_id):
    return User.query.get(user_id)

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def update_user(user, username=None, email=None):
    if username:
        user.username = username
    if email:
        user.email = email
    db.session.commit()
