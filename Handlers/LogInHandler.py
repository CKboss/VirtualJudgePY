import tornado.web
import tornado.gen

from tornado import concurrent

from tools.argCheck import argCheck
from tools.dbtools import getResult,Gao
from tools.dbcore import conn


class LogInHandler(tornado.web.RequestHandler) :

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):

        username = self.get_argument('username')
        password = self.get_argument('password')

        print(username,'   ',password)

        if argCheck(username) and argCheck(password) :
            ''''
            check = self.checkLogIn(username,password)
            print('check: ',check)
            '''
            cur = conn.cursor()
            print('now let\'s check')
            sql = 'select count(*) from user WHERE username = %s and password = %s'%(username,password)
            cnt = cur.execute(sql)
            print(cnt)

    ######################################################

    @concurrent.run_on_executor
    def checkLogIn(self,username,password):
        sql = 'select count(*) from user WHERE username = %s and password = %s'%(username,password)
        try :
            ret = getResult(sql)
            if len(ret) !=0 :
                print('pass check')
                return True
        except :
            print('error')
        print('fail check')
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

