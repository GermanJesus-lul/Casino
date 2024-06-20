import mysql.connector
import sqlite3
import os

import config

DBUSER = os.getenv('DBUSER')
DBPASS = os.getenv('DBPASS')

local = config.local()
db_host = config.db_host()
db_database = config.db_database()
db_path = config.db_path()


class SQL:
    def __init__(self, sql_type):
        self.sql_type = sql_type

    def __enter__(self):
        if not local:
            self.con = mysql.connector.connect(user=DBUSER, password=DBPASS,
                                               host=db_host, database=db_database)
            self.cur = self.con.cursor(buffered=True)
            return self.cur
        else:
            # local database
            self.con = sqlite3.connect(db_path)
            self.cur = self.con.cursor()
            return self.cur

    def __exit__(self, *args):
        if self.sql_type in ["INSERT", "UPDATE"]:
            self.con.commit()
        self.cur.close()
        self.con.close()
