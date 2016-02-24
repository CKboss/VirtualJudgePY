import pymysql
import sqlalchemy.pool as DBPool


def getConnection() :
    conn = pymysql.connect(
        host='localhost',
        user='javaTest',
        password='123456',
        db='mydb',
        charset='utf8',
        autocommit=True,
    )
    return conn

ConnPool = DBPool.QueuePool(getConnection,pool_size=50,max_overflow=100,timeout=25)

'''

conn = ConnPool.connect()

cur = conn.cursor()

ans = cur.execute('select * from user')

print(cur.fetchall())

'''

