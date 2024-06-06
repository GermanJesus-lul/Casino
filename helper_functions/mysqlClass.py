import mysql.connector
import os

DBUSER = os.getenv('DBUSER')
DBPASS = os.getenv('DBPASS')

class MySQL:
    def __init__(self, sql_type):
        self.sql_type = sql_type

    def __enter__(self):
        self.con = mysql.connector.connect(user=DBUSER, password=DBPASS,
                                           host='Betonblock.mysql.pythonanywhere-services.com',
                                           database='Betonblock$casino')
        self.cur = self.con.cursor(buffered=True)
        return self.cur

    def __exit__(self, *args):
        if self.sql_type in ["INSERT", "UPDATE"]:
            self.con.commit()
        self.cur.close()
        self.con.close()
