
'''
+-----------------+------------------+------+-----+---------+----------------+
| Field           | Type             | Null | Key | Default | Extra          |
+-----------------+------------------+------+-----+---------+----------------+
| uid             | int(10) unsigned | NO   | PRI | NULL    | auto_increment |
| username        | varchar(255)     | YES  | MUL | NULL    |                |
| nickname        | varchar(1024)    | YES  | MUL | NULL    |                |
| password        | char(50)         | NO   | MUL | NULL    |                |
| email           | varchar(255)     | YES  |     | NULL    |                |
| school          | varchar(255)     | YES  |     | NULL    |                |
| total_submit    | int(10) unsigned | NO   |     | NULL    |                |
| total_ac        | int(10) unsigned | NO   |     | NULL    |                |
| register_time   | datetime         | NO   |     | NULL    |                |
| last_login_time | datetime         | NO   |     | NULL    |                |
| photo           | varchar(255)     | YES  |     | NULL    |                |
| total_value     | int(10) unsigned | NO   |     | NULL    |                |
| lock_status     | tinyint(1)       | NO   |     | 0       |                |
| isroot          | int(11)          | NO   |     | NULL    |                |
| ipaddr          | varchar(255)     | YES  |     | NULL    |                |
| local_ac        | int(11)          | NO   |     | NULL    |                |
+-----------------+------------------+------+-----+---------+----------------+
'''

def checkUserSQL(username,passowrd):
    sql = 'select count(*) from user WHERE username = "%s" and password = "%s" '%(username,passowrd)
    return sql

def addUserSQL(**d):
    sql = 'INSERT INTO user (uid, username, nickname, password, email, school, total_submit, total_ac, register_time, last_login_time, photo, total_value, lock_status, isroot, ipaddr, local_ac)' \
          'VALUES (1,d[username],d[nicname],d[password],d[email],d[school],0,0,' ',' ',null,0,0,0,0,0)'
