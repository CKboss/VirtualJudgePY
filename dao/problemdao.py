'''
mysql> desc problem;
+-------------+---------------+------+-----+---------+----------------+
| Field       | Type          | Null | Key | Default | Extra          |
+-------------+---------------+------+-----+---------+----------------+
| pid         | int(11)       | NO   | PRI | NULL    | auto_increment |
| title       | varchar(255)  | YES  |     | NULL    |                |
| source      | varchar(255)  | YES  |     | NULL    |                |
| url         | varchar(1024) | YES  |     | NULL    |                |
| originOJ    | varchar(255)  | YES  |     | NULL    |                |
| originProb  | varchar(45)   | YES  |     | NULL    |                |
| memorylimit | varchar(45)   | YES  |     | NULL    |                |
| timelimit   | varchar(45)   | YES  |     | NULL    |                |
+-------------+---------------+------+-----+---------+----------------+

mysql> desc problemdetail;
+--------------+--------------+------+-----+---------+----------------+
| Field        | Type         | Null | Key | Default | Extra          |
+--------------+--------------+------+-----+---------+----------------+
| did          | int(11)      | NO   | PRI | NULL    | auto_increment |
| pid          | int(11)      | YES  | MUL | NULL    |                |
| description  | text         | YES  |     | NULL    |                |
| input        | text         | YES  |     | NULL    |                |
| output       | text         | YES  |     | NULL    |                |
| sampleinput  | text         | YES  |     | NULL    |                |
| sampleoutput | text         | YES  |     | NULL    |                |
| hint         | text         | YES  |     | NULL    |                |
| author       | varchar(255) | YES  |     | NULL    |                |
| source       | varchar(255) | YES  |     | NULL    |                |
| updateTime   | datetime     | YES  |     | NULL    |                |
+--------------+--------------+------+-----+---------+----------------+
'''
import pickle
import time
from tools.encode import Base64StrToUTF8Str, UTF8StrToBase64Str
from tools.dbcore import ConnPool
from tools.dbtools import getQuerySQL,getInserSQL, getUpdateSQL,FetchAll,FetchOne,ExeSQL


def GetProblemID(orj, orid):
    sql = 'SELECT problem.pid FROM problem WHERE ' \
          '( problem.originOJ LIKE "{}" AND problem.originProb LIKE "{}" )'.format(orj, orid)
    conn = ConnPool.connect()
    cur = conn.cursor()
    cur.execute(sql)
    tp = cur.fetchall()
    cur.close()
    conn.close()
    if tp.__len__() == 0:
        return 0
    else:
        return tp[0][0]


def pretreat_Problem(problem):
    pass
    '''
    if 'source' in problem :
        problem['source'] = UTF8StrToBase64Str(problem['source'])
    '''


def InsertProblem(problem):
    pretreat_Problem(problem)
    sql = getInserSQL('problem', problem)
    ExeSQL(sql)



def UpdateProblem(problem, pid):
    pretreat_Problem(problem)
    cluse = 'pid = {}'.format(pid)

    sql = getUpdateSQL('problem', data=problem, clause=cluse)

    #print('Update',sql)

    ExeSQL(sql)

def pretreat_ProblemDetail(problem):
    baselist = ['description', 'input', 'output', 'sampleinput', 'sampleoutput',
                'hint', 'author', 'source']

    for key in problem:
        if problem[key] is None:
            continue
        if key in baselist:
            problem[key] = UTF8StrToBase64Str(problem[key])


def InsertProblemDetail(problem):
    pretreat_ProblemDetail(problem)
    sql = getInserSQL('problemdetail', problem)
    ExeSQL(sql)


def UpdateProblemDetail(problem, pid):
    pretreat_ProblemDetail(problem)

    sql = getQuerySQL('problemdetail',' pid={} '.format(pid),' did ')
    rs = FetchOne(sql)

    if rs is None :
        InsertProblemDetail(problem)
    else :
        clause = 'problemdetail.pid = %d' % pid
        sql = getUpdateSQL('problemdetail', data=problem, clause=clause)
        ExeSQL(sql)


problem = dict(
    title=None,
    source=None,
    url=None,
    originOJ=None,
    originProb=None,
    virtualOJ=None,
    virtualProb=None,
)

problemdetail = dict(
    pid=None,
    description=None,
    input=None,
    output=None,
    sampleinput=None,
    sampleoutput=None,
    hint=None,
    author=None,
    source=None,
    updatetime=None,
    memorylimit=None,
    timelimit=None,
    specialjudge=False,
)


def InsertOrUpdateProblem(kwargs):
    pd = problem.copy()
    pdd = problemdetail.copy()

    for key in kwargs:
        if key in pd:
            pd[key] = kwargs[key]
        if key in pdd:
            pdd[key] = kwargs[key]

    pid = GetProblemID(pd['originOJ'], pd['originProb'])

    print('pid ---> ',pid)

    if pid == 0:
        # Insert problem table
        InsertProblem(pd)
        pid = GetProblemID(pd['originOJ'], pd['originProb'])
        pdd['pid'] = pid
        # Insert problemDetail title
        InsertProblemDetail(pdd)
    else:
        pdd['pid'] = pid
        # Update problem table
        print('Update problem table')
        UpdateProblem(pd, pid)
        # Update problemDetail table
        print('Update problemDetail table')
        UpdateProblemDetail(pdd, pid)

    '''
    print('-'*30)
    print(pd)
    print('-'*30)
    print(pdd)
    print('-'*30)
    '''


def test1():
    print(time.strftime('%Y-%m-%d %H:%M:%S'))

def main():
    f = open('/home/ckboss/Desktop/Development/testData/POJ/POJ_4050.pkl', 'rb')
    data = pickle.load(f)
    data['updatetime'] = time.strftime('%Y-%m-%d %H:%M:%S')
    InsertOrUpdateProblem(data)


'''
    f = open('/tmp/HDOJ5011.pkl','rb')
    data = pickle.load(f)
    InsertOrUpdateProblem(data)
'''

if __name__ == '__main__':
    #main()
    test1()
