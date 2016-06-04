import tornado.web

from dao.userdao import AddUser
from UIModule.MsgModule import renderMSG

from Config.ParametersConfig import SML_THREAD_POOL_SIZE
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

class RegisterHandler(tornado.web.RequestHandler):

    executor = ThreadPoolExecutor(SML_THREAD_POOL_SIZE)

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self, *args, **kwargs):

        dt = dict()

        dt['username'] = self.get_argument("username", None)
        dt['password'] = self.get_argument("password", None)
        repassword = self.get_argument("repassword", None)
        dt['email'] = self.get_argument("email", None)
        dt['school'] = self.get_argument('school', None)
        dt['localstatus'] = 0

        if dt['password'] != repassword:
            self.render('register.html')
        else:
            ret = yield self.AddUser(dt)
            if ret == 1:
                ''' success '''
                self.write(renderMSG('Regiest Success!!'))
                self.finish()
            else:
                ''' fail '''
                self.write(renderMSG('Regiest Fail !!!'))
                self.finish()
                return

    def get(self):
        self.render('register.html')

    @run_on_executor
    def AddUser(self,d):
        return AddUser(d)
