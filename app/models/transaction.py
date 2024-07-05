from datetime import datetime
from ..mysql_connector import db

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    to_account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    type = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
   
    # Add user_id if transactions need to be associated with a user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    from_account = db.relationship('Account', foreign_keys=[from_account_id], backref=db.backref('outgoing_transactions', lazy=True))
    to_account = db.relationship('Account', foreign_keys=[to_account_id], backref=db.backref('incoming_transactions', lazy=True))
