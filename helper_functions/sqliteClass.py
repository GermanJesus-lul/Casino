import sqlite3
import os

import config

DBUSER = os.getenv('DBUSER')
DBPASS = os.getenv('DBPASS')

db_path = config.db_path()


class SQL:
    def __init__(self, sql_type):
        self.sql_type = sql_type

    def __enter__(self):
        self.con = sqlite3.connect(db_path)
        self.cur = self.con.cursor()
        return self.cur

    def __exit__(self, *args):
        if self.sql_type in ["INSERT", "UPDATE"]:
            self.con.commit()
        self.cur.close()
        self.con.close()
