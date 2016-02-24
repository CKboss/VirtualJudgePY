import tornado.web
import tornado.gen

from tornado import concurrent

from tools.argCheck import argCheck
from tools.dbcore import ConnPool

from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

from dao.userdao import checkUserSQL,getUserUid

from Handlers.BaseHandler import BaseHandler

class LogInHandler(BaseHandler) :

    executor = ThreadPoolExecutor(4)

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):

        username = self.get_argument('username','None')
        password = self.get_argument('password','None')

        print(username,'   ',password)

        if argCheck(username) and argCheck(password) :
            isOK = yield self.checkPasswd(username,password)
            if  isOK is not None:
                self.set_secure_cookie('username',username)
                print('isOK: ',isOK)
                self.set_secure_cookie('uid',str(isOK))
                self.write('<h1>LogIn Success!</h1>')
            else :
                self.write('<h1>LogIn Fail</h1>')

        self.finish()



    @run_on_executor
    def checkPasswd(self,username,password):
        conn = ConnPool.connect()
        cur = conn.cursor()
        sql = checkUserSQL(username,password)
        print('exe: ',sql)
        cur.execute(sql)
        ans = cur.fetchall()
        print(ans)
        print(ans[0][0])
        if ans[0][0] == 1:
            sql = getUserUid(username)
            cur.execute(sql)
            uid = cur.fetchone()[0]
            cur.close()
            conn.close()
            return uid
        else :
            return None

if __name__=='__main__':
    username = 'parg1'
    password = 'parg2'
    #sql = 'select * from user WHERE username = %s and password = %s'%(username,password)
    sql = 'select * from user'
    print(sql)
    conn = ConnPool.connect()
    cur = conn.cursor()
    cur.execute(sql)
    conn.close()
    print(cur.fetchall())

