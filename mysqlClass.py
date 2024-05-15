import mysql.connector


class MySQL:
    def __init__(self, sql_type):
        self.sql_type = sql_type

    def __enter__(self):
        self.con = mysql.connector.connect(user='Betonblock', password='somepasswordformysql',
                                           host='Betonblock.mysql.pythonanywhere-services.com',
                                           database='Betonblock$casino')
        self.cur = self.con.cursor(buffered=True)
        return self.cur

    def __exit__(self, *args):
        if self.sql_type == "INSERT":
            self.con.commit()
        self.cur.close()
        self.con.close()
