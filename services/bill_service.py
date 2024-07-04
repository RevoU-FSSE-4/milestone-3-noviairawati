from models.bill import Bill
from mysql_connector import db

def create_bill(user_id, biller_name, due_date, amount, account_id):
    bill = Bill(user_id=user_id, biller_name=biller_name, due_date=due_date, amount=amount, account_id=account_id)
    db.session.add(bill)
    db.session.commit()
    return bill

def get_bill_by_id(bill_id):
    return Bill.query.get(bill_id)

def update_bill(bill, biller_name=None, due_date=None, amount=None, account_id=None):
    if biller_name:
        bill.biller_name = biller_name
    if due_date:
        bill.due_date = due_date
    if amount:
        bill.amount = amount
    if account_id:
        bill.account_id = account_id
    db.session.commit()

def delete_bill(bill):
    db.session.delete(bill)
    db.session.commit()
