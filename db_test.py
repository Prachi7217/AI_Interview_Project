import pyodbc

conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=localhost\\SQLEXPRESS;'
    'DATABASE=AI_Interview;'
    'Trusted_Connection=yes;'
)

print("Database Connected Successfully!")
