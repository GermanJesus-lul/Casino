import json
import sqlite3
import os

db_path = os.path.dirname(os.path.abspath(__file__)) + '/database.db'

os.remove(db_path)

# create local sqlite3 database
con = sqlite3.connect(db_path)
cur = con.cursor()
with open('sqlite_db.sql') as f:
    cur.executescript(f.read())
con.commit()
con.close()


config_json = {
    'local': True,
    'db_path': db_path
}

with open('config.json', 'w') as f:
    json.dump(config_json, f)
