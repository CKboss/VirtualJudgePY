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
from Handlers.DebugHandler import DebugHandler
from Handlers.ProblemListHandler import ProblemListHandler
from Handlers.RedirectorHandler import RedirectorHandler
from Handlers.SubmitHandler import SubmitHandler

from UIModule.HeaderModule import TitleModule
from UIModule.ProblemListModule import ProblemListModule

db = pymysql.connect(
   host='localhost',
   user='javaTest',
   password='123456',
   db='mydb',
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
            (r'/webdebug',DebugHandler),
            (r'/problemlist',ProblemListHandler),
            (r'/redirection',RedirectorHandler),
            (r'/submit\/{0,1}',SubmitHandler),
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

        UI_MODULES = dict(
            HeaderTitle = TitleModule,
            ProblemList = ProblemListModule,
        )

        tornado.web.Application.__init__(self, handlers,ui_modules=UI_MODULES, **settings)

if __name__=='__main__':
    print(os.path.join(os.path.pardir,'templates'))
    print(os.path.join(os.path.pardir,'statics'))
