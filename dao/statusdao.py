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


rankSLQ = '''
    SELECT rank,uname,acnum,trynum,radio,motto
    FROM (
        SELECT (@rank := @rank+1) as rank,uname,motto,acnum,trynum,radio
        FROM (
               SELECT
                 username                                            AS uname,
                 nickname                                             AS motto,
                 (SELECT COUNT(DISTINCT pid)
                  FROM status
                  WHERE username = uname AND status LIKE '%accept%') AS acnum,
                 (SELECT COUNT(DISTINCT pid)
                  FROM status
                  WHERE username = uname)                            AS trynum,
                 (SELECT IFNULL(TRUNCATE(acnum / trynum, 6), 0))     AS radio
               FROM user
               ORDER BY acnum DESC, radio DESC, trynum DESC, uname
             ) as TEMPTABLE , (SELECT @rank := 0) as r
    ) AS TEMPTABLE2
'''

def GetAuthorsRank(page,pagelimit) :

    sql = rankSLQ+'LIMIT {},{};'.format(pagelimit*page,pagelimit+1)
    return FetchAll(sql)

def GetUserRank(username) :

    sql = rankSLQ+'WHERE uname = "{}";'.format(username)
    return FetchAll(sql)[0]

if __name__ == '__main__' :
    #rs = GetAuthorsRank(0,1)
    rs = GetUserRank('test2')
    print(rs)
    #print(int(rs[0][0]),rs[0][4])
