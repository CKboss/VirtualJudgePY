import tornado.web
import tornado.gen

from tornado import concurrent

from tools.argCheck import argCheck
from tools.dbcore import conn


class LogInHandler(tornado.web.RequestHandler) :

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):

        username = self.get_argument('username','None')
        password = self.get_argument('password','None')

        print(username,'   ',password)

        if argCheck(username) and argCheck(password) :
            if self.checkPasswd(username,password) == True :
                self.set_secure_cookie("username",username)
                self.redirect('/')
            else :
                self.redirect('/fail')


    def checkPasswd(self,username,password):
        cur = conn.cursor()
        sql = 'select count(*) from user WHERE username = "%s" and password = "%s" '%(username,password)
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

