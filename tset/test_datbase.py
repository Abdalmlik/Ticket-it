import pyodbc

conn_str = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=ahesham-pc\AHESHAM;"
    "Database=Ticket_it;"
    "Trusted_Connection=yes;"
)
try:
    conn = pyodbc.connect(conn_str)
    print("Connection successful!")
except Exception as e:
    print(f"Connection failed: {e}")
