from models.budget import Budget
from mysql_connector import db

def create_budget(user_id, name, amount, start_date, end_date):
    budget = Budget(user_id=user_id, name=name, amount=amount, start_date=start_date, end_date=end_date)
    db.session.add(budget)
    db.session.commit()
    return budget

def get_budget_by_id(budget_id):
    return Budget.query.get(budget_id)

def update_budget(budget, name=None, amount=None, start_date=None, end_date=None):
    if name:
        budget.name = name
    if amount:
        budget.amount = amount
    if start_date:
        budget.start_date = start_date
    if end_date:
        budget.end_date = end_date
    db.session.commit()

def delete_budget(budget):
    db.session.delete(budget)
    db.session.commit()
