# -*- coding: utf-8 -*-

"""
This is dbConnector.
To use this module, you need to make MySQLdb instance in advance.
ex)
  CONNECTION = MySQLdb.connect(
    host = '127.0.0.1',
    db = 'xxxxx',
    user = 'xxxxx',
    passwd = 'xxxxx')
"""

import MySQLdb
from MySQLdb import connect,cursors

# connection with mysql
def connection(conn):
    conn.cursorclass = MySQLdb.cursors.DictCursor
    return conn.cursor()

class DbConnector:

    def __init__(self, connection):
        self.conn = connection
#        self.conn = connect(host,db,user,passwd)
        self.cur = self.conn.cursor(cursors.DictCursor)


    # insert record from sql
    def insertRecord(self,sql):
        self.cur.execute(sql)
        self.conn.commit()


    # fetch records from sql
    def fetchRecords(self,sql):
        self.cur.execute(sql)
        return self.cur.fetchall()


    # update records from sql
    def updateRecords(self,sql):
        self.cur.execute(sql)
        self.conn.commit()

    # delete record from sql
    def deleteRecords(self,sql):
        self.execute(sql)
        self.conn.commit()

# doing from console(test mode)
if __name__ == '__main__':
    mysql = MySqlConnection(
            "",
            "",
            "",
            "",
            "utf8")
    sql = "SELECT * FROM user_list"
    record = mysql.fetchRecords(sql)
    print record
