from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_bcrypt import Bcrypt
from app.models import db, User, Ticket, ActivityLog
from datetime import datetime
from sqlalchemy import or_

# Define a Blueprint for routes
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

    # Fetch tickets created or assigned to the logged-in user
    tickets = Ticket.query.filter(
        or_(Ticket.CreatedBy == session['user_id'], Ticket.AssignedTo == session['user_id'])
    ).all()

    return render_template('dashboard.html', tickets=tickets)

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

# Create Ticket Route
@bp.route('/create_ticket', methods=['GET', 'POST'])
def create_ticket():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        category = request.form['category']
        priority = request.form['priority']
        status = request.form['status']

        # Get the ID of the logged-in user (assumes you use Flask-Login)
        created_by = current_user.UserID  # Flask-Login's current_user is assumed

        # Validate Category
        valid_categories = ['Hardware', 'Software', 'Network', 'Other']
        if category not in valid_categories:
            flash('Invalid category. Please choose one of the valid categories: Hardware, Software, Network, or Other.', 'danger')
            return redirect(url_for('routes.create_ticket'))  # Return to the ticket creation page

        # Validate Priority
        valid_priorities = ['Low', 'Medium', 'High']
        if priority not in valid_priorities:
            flash('Invalid priority. Please choose one of the valid priorities: Low, Medium, or High.', 'danger')
            return redirect(url_for('routes.create_ticket'))  # Return to the ticket creation page

        # Create a new Ticket instance
        new_ticket = Ticket(
            Title=title,
            Description=description,
            Category=category,   # Validated category
            Priority=priority,   # Validated priority
            Status=status,
            CreatedBy=created_by,
        )

        # Add to session and commit
        db.session.add(new_ticket)
        db.session.commit()

        flash('Ticket created successfully!', 'success')
        return redirect(url_for('routes.view_tickets'))

    return render_template('create_ticket.html')

# View Ticket Route (view details of a specific ticket)
@bp.route('/ticket/<int:ticket_id>')
def view_ticket(ticket_id):
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))

    ticket = Ticket.query.get_or_404(ticket_id)
    if ticket.UserID != session['user_id']:
        flash('You do not have permission to view this ticket.', 'danger')
        return redirect(url_for('routes.dashboard'))

    return render_template('view_ticket.html', ticket=ticket)

# Update Ticket Route
@bp.route('/update_ticket/<int:ticket_id>', methods=['GET', 'POST'])
def update_ticket(ticket_id):
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))

    ticket = Ticket.query.get_or_404(ticket_id)
    if ticket.UserID != session['user_id']:
        flash('You do not have permission to update this ticket.', 'danger')
        return redirect(url_for('routes.dashboard'))

    if request.method == 'POST':
        ticket.Title = request.form['title']
        ticket.Description = request.form['description']
        ticket.Status = request.form['status']  # You can add options like 'Open', 'In Progress', 'Closed'
        db.session.commit()

        flash('Ticket updated successfully!', 'success')
        return redirect(url_for('routes.view_ticket', ticket_id=ticket_id))

    return render_template('update_ticket.html', ticket=ticket)

# Delete Ticket Route
@bp.route('/delete_ticket/<int:ticket_id>', methods=['POST'])
def delete_ticket(ticket_id):
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))

    ticket = Ticket.query.get_or_404(ticket_id)
    if ticket.UserID != session['user_id']:
        flash('You do not have permission to delete this ticket.', 'danger')
        return redirect(url_for('routes.dashboard'))

    db.session.delete(ticket)
    db.session.commit()

    flash('Ticket deleted successfully!', 'success')
    return redirect(url_for('routes.dashboard'))

