import mysql.connector
import sqlite3
import os

from config import LOCAL

DBUSER = os.getenv('DBUSER')
DBPASS = os.getenv('DBPASS')


class SQL:
    def __init__(self, sql_type):
        self.sql_type = sql_type

    def __enter__(self):
        if not LOCAL:
            self.con = mysql.connector.connect(user=DBUSER, password=DBPASS,
                                               host='Betonblock.mysql.pythonanywhere-services.com',
                                               database='Betonblock$casino')
            self.cur = self.con.cursor(buffered=True)
            return self.cur
        else:
            # local database
            self.con = sqlite3.connect('/Users/juliusgoler/python_projects/Casino/database.db')
            self.cur = self.con.cursor()
            return self.cur

    def __exit__(self, *args):
        if self.sql_type in ["INSERT", "UPDATE"]:
            self.con.commit()
        self.cur.close()
        self.con.close()
