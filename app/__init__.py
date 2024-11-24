from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    # Add SECRET_KEY for session handling
    app.config['SECRET_KEY'] = 'your-secure-secret-key'  # Replace with a strong key
    app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc://ahesham-pc\\AHESHAM/Ticket_it?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)  # Initialize Flask-Login

    # Configure LoginManager
    login_manager.login_view = 'routes.login'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # Fetch user by ID

    with app.app_context():
        db.create_all()  # Ensure tables are created

        # Register routes
        from app.routes import bp as routes_blueprint
        app.register_blueprint(routes_blueprint)

    return app
