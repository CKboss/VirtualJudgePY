'''
+------------+--------------+------+-----+---------+----------------+
| Field      | Type         | Null | Key | Default | Extra          |
+------------+--------------+------+-----+---------+----------------+
| runid      | int(11)      | NO   | PRI | NULL    | auto_increment |
| timesubmit | datetime     | YES  |     | NULL    |                |
| status     | varchar(100) | YES  |     | NULL    |                |
| runtime    | varchar(45)  | YES  |     | NULL    |                |
| runmemory  | varchar(45)  | YES  |     | NULL    |                |
| pid        | int(11)      | YES  | MUL | NULL    |                |
| cid        | int(11)      | YES  |     | NULL    |                |
| language   | varchar(45)  | YES  |     | NULL    |                |
| source     | text         | YES  |     | NULL    |                |
| isopen     | tinyint(1)   | YES  |     | NULL    |                |
| uid        | int(11)      | YES  |     | NULL    |                |
| username   | varchar(255) | YES  |     | NULL    |                |
| originOJ   | varchar(255) | YES  |     | NULL    |                |
| originProb | varchar(45)  | YES  |     | NULL    |                |
| realrunid  | varchar(45)  | YES  |     | NULL    |                |
| isdisplay  | tinyint(1)   | YES  |     | NULL    |                |
| ceinfo     | text         | YES  |     | NULL    |                |
+------------+--------------+------+-----+---------+----------------+
'''

from tools.dbcore import ConnPool
from tools.dbtools import FetchAll,FetchOne

def CheckIfAccept(uid,pid,cid=-1) :

    sql = 'SELECT count(DISTINCT pid) FROM status WHERE uid = {} and pid = {} and status like "%accept%";'.format(uid,pid)
    return FetchOne(sql)

def CheckIfTry(uid,pid):
    sql = 'SELECT count(DISTINCT pid) FROM status WHERE uid = {} and pid = {};'.format(uid,pid)
    return FetchOne(sql)


def CountContestSubmitNum(cid) :

    sql = 'SELECT pid,COUNT(*) FROM status WHERE cid = {} GROUP BY pid;'.format(cid)
    return FetchAll(sql)

def CountContestACNum(cid):

    sql = 'SELECT pid,COUNT(*) FROM status WHERE cid = {} and status LIKE "%accept%" GROUP BY pid;'.format(cid)
    return FetchAll(sql)


def CheckContestIfAccept(uid,pid,cid) :

    sql = 'SELECT count(DISTINCT pid) FROM status WHERE uid = {} and pid = {} and cid = {} and status like "%accept%";'.format(uid,pid,cid)
    return FetchOne(sql)


def CheckContestIfTry(uid,pid,cid):
    sql = 'SELECT count(DISTINCT pid) FROM status WHERE uid = {} and pid = {} AND cid = {} ;'.format(uid,pid,cid)
    return FetchOne(sql)
