import sqlite3
import os
from argon2 import PasswordHasher

# Ensure the database directory exists
db_dir = os.path.join(os.getcwd(), 'database')
os.makedirs(db_dir, exist_ok=True)

# Set the database path within the mounted volume
db_path = os.path.join(db_dir, 'mydatabase.db')

# Create local sqlite3 database
con = sqlite3.connect(db_path)
cur = con.cursor()
with open('/app/sqlite_db.sql') as f:
    cur.executescript(f.read())
con.commit()

# Add testing user (test:test)
ph = PasswordHasher()
phash = ph.hash("test")
cur.execute(f'INSERT INTO users (username, password, balance) VALUES ("test", "{phash}", 100)')
con.commit()

con.close()