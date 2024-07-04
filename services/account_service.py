from models.account import Account
from mysql_connector import db

def create_account(user_id, account_type, account_number, balance):
    account = Account(user_id=user_id, account_type=account_type, account_number=account_number, balance=balance)
    db.session.add(account)
    db.session.commit()
    return account

def get_account_by_id(account_id):
    return Account.query.get(account_id)

def update_account(account, account_type=None, account_number=None, balance=None):
    if account_type:
        account.account_type = account_type
    if account_number:
        account.account_number = account_number
    if balance is not None:
        account.balance = balance
    db.session.commit()

def delete_account(account):
    db.session.delete(account)
    db.session.commit()
