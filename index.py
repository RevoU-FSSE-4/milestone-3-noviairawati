from flask import Flask, jsonify
from config import Config
from mysql_connector import db
from routes import user_bp, account_bp, transaction_bp, budget_bp, bill_bp

app = Flask(__name__)
app.config.from_object(Config)

# Initialize SQLAlchemy with the Flask app
db.init_app(app)

# Register blueprints
app.register_blueprint(user_bp)
app.register_blueprint(account_bp)
app.register_blueprint(transaction_bp)
app.register_blueprint(budget_bp)
app.register_blueprint(bill_bp)

# Test database connection endpoint
@app.route('/test_db_connection')
def test_db_connection():
    try:
        # Try to execute a query to ensure the database connection is working
        db.session.execute('SELECT 1')
        return "Database connection successful!", 200
    except Exception as e:
        app.logger.error(f"Database connection error: {e}")
        return jsonify({'error': 'Database connection error'}), 500

# Create database tables if running the script directly
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables based on the models
    app.run(debug=True)
