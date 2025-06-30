import sqlite3

conn = sqlite3.connect('instance/attendees.db')  # Ensure this is the correct path to your database
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Tables in database:", tables)

conn.close()
