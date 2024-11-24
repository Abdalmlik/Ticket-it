from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_bcrypt import Bcrypt
from app.models import db, User, Ticket, ActivityLog
from datetime import datetime

# Define a Blueprint
bp = Blueprint('routes', __name__)
bcrypt = Bcrypt()

# Home Route
@bp.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('routes.dashboard'))
    return render_template('login.html')

# Define a Blueprint
bp = Blueprint('routes', __name__)
bcrypt = Bcrypt()

# Home Route
@bp.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('routes.dashboard'))
    return render_template('login.html')

# Login Route
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(Email=email).first()

        if user and bcrypt.check_password_hash(user.PasswordHash, password):
            session['user_id'] = user.UserID
            session['role'] = user.Role
            flash('Login successful!', 'success')
            return redirect(url_for('routes.dashboard'))
        flash('Invalid email or password', 'danger')

    return render_template('login.html')

# Logout Route
@bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('routes.login'))

# Dashboard Route
@bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))

    return render_template('dashboard.html')

# Register Route (to create a user)
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role'] or 'User'  # Default role

        # Check if email already exists
        if User.query.filter_by(Email=email).first():
            flash('Email already registered.', 'danger')
            return redirect(url_for('routes.register'))

        # Hash the password before saving
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Save the user to the database
        new_user = User(Name=name, Email=email, PasswordHash=hashed_password, Role=role)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('routes.login'))

    return render_template('register.html')

# Other routes (create_ticket, view_ticket, update_ticket, delete_ticket) follow the same structure...
