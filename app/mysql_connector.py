from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()


def init_db():
    from .models.user import User
    from .models.account import Account
    from .models.transaction import Transaction
    from .models.budget import Budget
    from .models.bill import Bill

    db.create_all()
