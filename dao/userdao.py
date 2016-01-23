'''
+-------------+---------------+------+-----+---------+----------------+
| Field       | Type          | Null | Key | Default | Extra          |
+-------------+---------------+------+-----+---------+----------------+
| uid         | int(11)       | NO   | PRI | NULL    | auto_increment |
| username    | varchar(255)  | YES  |     | NULL    |                |
| nickname    | varchar(1024) | YES  |     | NULL    |                |
| password    | varchar(50)   | YES  |     | NULL    |                |
| email       | varchar(255)  | YES  |     | NULL    |                |
| school      | varchar(255)  | YES  |     | NULL    |                |
| localstatus | tinyint(1)    | YES  |     | NULL    |                |
+-------------+---------------+------+-----+---------+----------------+
'''

from tools.dbtools import getInserSQL
from tools.dbcore import conn

def checkUserSQL(username,passowrd):
    sql = 'select count(*) from user WHERE username = "%s" and password = "%s" '%(username,passowrd)
    return sql

def checkUserExist(username) :
    sql = 'select count(*) from user WHERE username = "%s"'%(username)
    return sql

def AddUser(d):
    sql = getInserSQL('user',d)
    cur = conn.cursor()
    ret = cur.execute(sql)
    return ret

if __name__=='__main__':
    pass
