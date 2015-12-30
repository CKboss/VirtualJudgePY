
from tornado import gen,ioloop
from tornado_mysql import pools


pools.DEBUG=True

POOL = pools.Pool(
    dict(
        host='127.0.0.1', port=3306, user='javaTest', passwd='123456', db='test',
    ),
    max_idle_connections=5,
    max_recycle_sec=10,
    max_open_connections=15,
)

class theSQL:
    sql = 'select * from user'

@gen.coroutine
def Gao():
    cur = yield POOL.execute(theSQL.sql)
    return cur.fetchall()

def getResult(sql):
    theSQL.sql=sql
    return ioloop.IOLoop.current().run_sync(Gao)

if __name__=='__main__' :
    ans = getResult('select * from user')
    print(ans)
