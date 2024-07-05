from datetime import datetime
from ..mysql_connector import db

class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    biller_name = db.Column(db.String(255), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('bills', lazy=True))
    account = db.relationship('Account', backref=db.backref('bills', lazy=True))
