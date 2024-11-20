from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_bcrypt import Bcrypt
from app.models import db, User, Ticket, ActivityLog
from datetime import datetime

bcrypt = Bcrypt()

# Home Route
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(Email=email).first()

        if user and bcrypt.check_password_hash(user.PasswordHash, password):
            session['user_id'] = user.UserID
            session['role'] = user.Role
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid email or password', 'danger')

    return render_template('login.html')

# Logout Route
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Dashboard Route
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    tickets = Ticket.query.filter_by(CreatedBy=session['user_id']).all()
    return render_template('dashboard.html', tickets=tickets)

# Create Ticket Route
@app.route('/ticket/create', methods=['GET', 'POST'])
def create_ticket():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        category = request.form['category']
        priority = request.form['priority']
        
        # Create a new ticket in the database
        new_ticket = Ticket(
            Title=title,
            Description=description,
            Category=category,
            Priority=priority,
            CreatedBy=session['user_id'],
        )
        db.session.add(new_ticket)
        db.session.commit()

        # Log the activity (ticket creation)
        activity_log = ActivityLog(
            TicketID=new_ticket.TicketID,
            Action="Created a new ticket",
            PerformedBy=session['user_id'],
            Timestamp=datetime.utcnow()
        )
        db.session.add(activity_log)
        db.session.commit()

        flash('Ticket created successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('create_ticket.html')

# View Ticket Route (for individual tickets)
@app.route('/ticket/<int:ticket_id>')
def view_ticket(ticket_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    ticket = Ticket.query.get_or_404(ticket_id)
    return render_template('view_ticket.html', ticket=ticket)

# Update Ticket Route (e.g., for changing the status)
@app.route('/ticket/<int:ticket_id>/update', methods=['GET', 'POST'])
def update_ticket(ticket_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    ticket = Ticket.query.get_or_404(ticket_id)

    if request.method == 'POST':
        ticket.Status = request.form['status']
        db.session.commit()

        # Log the update activity
        activity_log = ActivityLog(
            TicketID=ticket.TicketID,
            Action=f"Updated ticket status to {ticket.Status}",
            PerformedBy=session['user_id'],
            Timestamp=datetime.utcnow()
        )
        db.session.add(activity_log)
        db.session.commit()

        flash(f"Ticket status updated to {ticket.Status}!", 'success')
        return redirect(url_for('view_ticket', ticket_id=ticket.TicketID))

    return render_template('update_ticket.html', ticket=ticket)

# Delete Ticket Route
@app.route('/ticket/<int:ticket_id>/delete', methods=['POST'])
def delete_ticket(ticket_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    ticket = Ticket.query.get_or_404(ticket_id)

    db.session.delete(ticket)
    db.session.commit()

    # Log the delete activity
    activity_log = ActivityLog(
        TicketID=ticket.TicketID,
        Action="Deleted ticket",
        PerformedBy=session['user_id'],
        Timestamp=datetime.utcnow()
    )
    db.session.add(activity_log)
    db.session.commit()

    flash('Ticket deleted successfully!', 'success')
    return redirect(url_for('dashboard'))
