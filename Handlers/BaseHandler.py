import tornado.web

class BaseHandler(tornado.web.RequestHandler) :

    def prepare(self):
        self.get_current_user()

    def get_current_user(self):

        self.current_user = self.get_secure_cookie('username')

        if self.current_user is None :
            self.current_user = ''
        else :
            self.current_user=self.current_user.decode('utf-8')
