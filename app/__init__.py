from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc://ahesham-pc\AHESHAM/Ticket_it?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()  # Ensure tables are created

    return app
