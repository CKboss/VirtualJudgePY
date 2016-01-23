import tornado.web

from dao.userdao import AddUser

class RegisterHandler(tornado.web.RequestHandler):

    def post(self, *args, **kwargs):

        dt = dict()

        dt['username'] = self.get_argument("username",None)
        dt['password'] = self.get_argument("password",None)
        repassword = self.get_argument("repassword",None)
        dt['email'] = self.get_argument("email",None)
        dt['school'] = self.get_argument('school',None)
        dt['localstatus'] = 0

        if dt['password']!=repassword :
            self.render('register.html')
        else :
            ret = AddUser(dt)
            if ret==1 :
                ''' success '''
            else :
                ''' fail '''

    def get(self):
        self.render('register.html')
