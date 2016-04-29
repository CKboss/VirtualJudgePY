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
from tools.dbcore import ConnPool
from tools.encode import SHA512


def checkUserSQL(username, password):
    password = SHA512(username+'@'+password)
    sql = 'select count(*) from user WHERE username = "%s" and password = "%s" ' % (username, password)
    return sql


def getUserUid(username):
    sql = 'select uid from user WHERE username="%s"' % (username)
    return sql


def checkUserExist(username):
    sql = 'select count(*) from user WHERE username = "%s"' % (username)
    return sql


def AddUser(d):
    conn = ConnPool.connect()
    cur = conn.cursor()

    sql = checkUserExist(d['username'])
    cur.execute(sql)
    ret = cur.fetchone()
    if ret[0] != 0:
        return 0

    d['password'] = SHA512(d['username']+'@'+d['password'])

    sql = getInserSQL('user', d)
    ret = cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
    return ret


if __name__ == '__main__':
    pass
