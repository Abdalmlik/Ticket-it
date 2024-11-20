from . import db

class User(db.Model):
    __tablename__ = 'Users'
    UserID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(150), unique=True, nullable=False)
    PasswordHash = db.Column(db.String(255), nullable=False)
    Role = db.Column(db.String(50), nullable=False)

class Ticket(db.Model):
    __tablename__ = 'Tickets'
    TicketID = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(255), nullable=False)
    Description = db.Column(db.Text, nullable=False)
    Category = db.Column(db.String(50), nullable=False)
    Priority = db.Column(db.String(50), default='Low')
    Status = db.Column(db.String(50), default='Open')
    CreatedBy = db.Column(db.Integer, db.ForeignKey('Users.UserID'), nullable=False)
    AssignedTo = db.Column(db.Integer, db.ForeignKey('Users.UserID'), nullable=True)
    CreatedAt = db.Column(db.DateTime, default=db.func.current_timestamp())
    UpdatedAt = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class ActivityLog(db.Model):
    __tablename__ = 'ActivityLogs'
    LogID = db.Column(db.Integer, primary_key=True)
    TicketID = db.Column(db.Integer, db.ForeignKey('Tickets.TicketID'), nullable=False)
    Action = db.Column(db.String(255), nullable=False)
    PerformedBy = db.Column(db.Integer, db.ForeignKey('Users.UserID'), nullable=False)
    Timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

class Attachment(db.Model):
    __tablename__ = 'Attachments'
    AttachmentID = db.Column(db.Integer, primary_key=True)
    TicketID = db.Column(db.Integer, db.ForeignKey('Tickets.TicketID'), nullable=False)
    FilePath = db.Column(db.String(255), nullable=False)
    UploadedBy = db.Column(db.Integer, db.ForeignKey('Users.UserID'), nullable=False)
    UploadedAt = db.Column(db.DateTime, default=db.func.current_timestamp())
