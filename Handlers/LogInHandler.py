import tornado.web
import tornado.gen

from tornado import concurrent

from tools.argCheck import argCheck
from tools.dbcore import conn

from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

from dao.userdao import checkUserSQL

class LogInHandler(tornado.web.RequestHandler) :

    executor = ThreadPoolExecutor(4)

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):

        username = self.get_argument('username','None')
        password = self.get_argument('password','None')

        print(username,'   ',password)

        if argCheck(username) and argCheck(password) :
            isOK = yield self.checkPasswd(username,password)
            if  isOK == True :
                self.set_secure_cookie("username",username)
                self.redirect('/')
            else :
                self.redirect('/fail')


    @run_on_executor
    def checkPasswd(self,username,password):
        cur = conn.cursor()
        sql = checkUserSQL(username,password)
        print('exe: ',sql)
        cur.execute(sql)
        ans = cur.fetchall()
        print(ans)
        print(ans[0][0])
        if ans[0][0] == 1:
            return True
        else :
            return False

if __name__=='__main__':
    username = 'parg1'
    password = 'parg2'
    #sql = 'select * from user WHERE username = %s and password = %s'%(username,password)
    sql = 'select * from user'
    print(sql)
    cur = conn.cursor()
    cur.execute(sql)
    print(cur.fetchall())

