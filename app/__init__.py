from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask App and Database
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a strong key
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        'mssql+pyodbc://username:password@server_name/database_name?driver=ODBC+Driver+17+for+SQL+Server'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()  # Create tables based on models

    return app
