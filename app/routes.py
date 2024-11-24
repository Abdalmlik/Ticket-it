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

    tickets = Ticket.query.filter_by(CreatedBy=session['user_id']).all()
    return render_template('dashboard.html', tickets=tickets)

# Other routes (create_ticket, view_ticket, update_ticket, delete_ticket) follow the same structure...
