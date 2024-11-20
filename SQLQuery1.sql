CREATE DATABASE Ticket_it;

USE Ticket_it;

CREATE TABLE Users (
    UserID INT IDENTITY(1,1) PRIMARY KEY,
    Name NVARCHAR(100) NOT NULL,
    Email NVARCHAR(150) NOT NULL UNIQUE,
    PasswordHash NVARCHAR(255) NOT NULL,
    Role NVARCHAR(50) CHECK (Role IN ('Admin', 'Support Agent', 'Regular User')) NOT NULL,
    CreatedAt DATETIME DEFAULT GETDATE()
);

CREATE TABLE Tickets (
    TicketID INT IDENTITY(1,1) PRIMARY KEY,
    Title NVARCHAR(255) NOT NULL,
    Description NVARCHAR(MAX) NOT NULL,
    Category NVARCHAR(50) CHECK (Category IN ('Hardware', 'Software', 'Network', 'Other')) NOT NULL,
    Priority NVARCHAR(50) CHECK (Priority IN ('Low', 'Medium', 'High')) DEFAULT 'Low',
    Status NVARCHAR(50) CHECK (Status IN ('Open', 'In Progress', 'Closed')) DEFAULT 'Open',
    CreatedBy INT NOT NULL,
    AssignedTo INT NULL,
    CreatedAt DATETIME DEFAULT GETDATE(),
    UpdatedAt DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (CreatedBy) REFERENCES Users(UserID),
    FOREIGN KEY (AssignedTo) REFERENCES Users(UserID)
);

CREATE TABLE ActivityLogs (
    LogID INT IDENTITY(1,1) PRIMARY KEY,
    TicketID INT NOT NULL,
    Action NVARCHAR(255) NOT NULL,
    PerformedBy INT NOT NULL,
    Timestamp DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (TicketID) REFERENCES Tickets(TicketID),
    FOREIGN KEY (PerformedBy) REFERENCES Users(UserID)
);

CREATE TABLE Attachments (
    AttachmentID INT IDENTITY(1,1) PRIMARY KEY,
    TicketID INT NOT NULL,
    FilePath NVARCHAR(255) NOT NULL,
    UploadedBy INT NOT NULL,
    UploadedAt DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (TicketID) REFERENCES Tickets(TicketID),
    FOREIGN KEY (UploadedBy) REFERENCES Users(UserID)
);

CREATE TABLE Reports (
    ReportID INT IDENTITY(1,1) PRIMARY KEY,
    Title NVARCHAR(255) NOT NULL,
    ReportData NVARCHAR(MAX) NOT NULL,
    GeneratedBy INT NOT NULL,
    GeneratedAt DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (GeneratedBy) REFERENCES Users(UserID)
);
USE Ticket_it;
GO
ALTER AUTHORIZATION ON DATABASE::Ticket_it TO [ETTC\Abdalmalek.Hesham];
