import json
import sqlite3
import os
from argon2 import PasswordHasher

db_path = os.path.dirname(os.path.abspath(__file__)) + '/database.db'

try:
    os.remove(db_path)
except FileNotFoundError:
    pass

# create local sqlite3 database
con = sqlite3.connect(db_path)
cur = con.cursor()
with open('sqlite_db.sql') as f:
    cur.executescript(f.read())
con.commit()

# add testing user (test:test)
ph = PasswordHasher()
phash = ph.hash("test")
cur.execute(f'INSERT INTO users (username, password, balance) VALUES ("test", "{phash}", 100)')
con.commit()

con.close()


with open('config.json', 'r') as f:
    config_json = json.load(f)

config_json["local"] = True
config_json["db_path"] = db_path

with open('config.json', 'w') as f:
    json.dump(config_json, f)
