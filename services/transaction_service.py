from models.transaction import Transaction
from mysql_connector import db

def create_transaction(from_account_id, to_account_id, amount, type, description):
    transaction = Transaction(from_account_id=from_account_id, to_account_id=to_account_id, amount=amount, type=type, description=description)
    db.session.add(transaction)
    db.session.commit()
    return transaction

def get_transaction_by_id(transaction_id):
    return Transaction.query.get(transaction_id)

def delete_transaction(transaction):
    db.session.delete(transaction)
    db.session.commit()
