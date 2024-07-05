from flask import Flask
from .config import Config
from .mysql_connector import db
from .routes import (
    user_routes,
    account_routes,
    transaction_routes,
    budget_routes,
    bill_routes,
)
from flask_login import LoginManager


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    from .models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(user_routes.bp)
    app.register_blueprint(account_routes.bp)
    app.register_blueprint(transaction_routes.bp)
    app.register_blueprint(budget_routes.bp)
    app.register_blueprint(bill_routes.bp)

    return app
