from app import create_app
from app.mysql_connector import db

app = create_app()
with app.app_context():
    db.create_all()

    from app import create_app

if __name__ == '__main__':
    app.run(debug=True)
