from .user_routes import user_bp
from .account_routes import account_bp
from .transaction_routes import transaction_bp
from .budget_routes import budget_bp
from .bill_routes import bill_bp

def register_routes(app):
    app.register_blueprint(user_bp)
    app.register_blueprint(account_bp)
    app.register_blueprint(transaction_bp)
    app.register_blueprint(budget_bp)
    app.register_blueprint(bill_bp)
