import os.path

import tornado.web
import pymysql

from tornado.options import options,define
define('port',default=48888,help='the open port',type=int)

from Handlers.IndexHandler import IndexHandler
from Handlers.LogInHandler import LogInHandler
from Handlers.LogOutHandler import LogOutHandler
from Handlers.RegisterHandler import RegisterHandler
from Handlers.ProblemHandler import ProblemHandler
from Handlers.StatusHandler import StatusHandler

db = pymysql.connect(
   host='localhost',
   user='javaTest',
   password='123456',
   db='test',
   charset='utf8',
   cursorclass=pymysql.cursors.DictCursor
)

class AppInit(tornado.web.Application) :

    def __init__(self):

        # Url To Handler
        handlers = [
            (r'/',IndexHandler),
            (r'/login\/{0,1}',LogInHandler),
            (r'/logout\/{0,1}',LogOutHandler),
            (r'/register\/{0,1}',RegisterHandler),
            (r'/problem/(\w+)/(\w+)',ProblemHandler),
            (r'/status\/{0,1}',StatusHandler),
        ]

        # Setting
        settings = dict(

            template_path = os.path.join(os.path.pardir,'VirtualJudgePY/templates'),
            static_path = os.path.join(os.path.pardir,'VirtualJudgePY/statics'),
            debug = True,
            gzip = True,
            xsrf_cookies = True,
           	cookie_secret = 'tZJnmMPUSsyQYlXKOWWDVJbuW6Ul9k8IhZ8gF7Aq87E=',
        )

        tornado.web.Application.__init__(self,handlers,**settings)

if __name__=='__main__':
    print(os.path.join(os.path.pardir,'templates'))
    print(os.path.join(os.path.pardir,'statics'))
