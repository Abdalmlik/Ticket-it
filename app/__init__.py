from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)

    # Add SECRET_KEY for session handling
    app.config['SECRET_KEY'] = 'your-secure-secret-key'  # Replace with a strong key
    app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc://ahesham-pc\\AHESHAM/Ticket_it?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bcrypt.init_app(app)  # Ensure Bcrypt is initialized

    with app.app_context():
        db.create_all()  # Ensure tables are created

        # Register routes
        from app.routes import bp as routes_blueprint
        app.register_blueprint(routes_blueprint)

    return app
