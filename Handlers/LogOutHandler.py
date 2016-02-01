import tornado.web

class LogOutHandler(tornado.web.RequestHandler) :

    def post(self, *args, **kwargs):
        self.set_secure_cookie('username','',0)
        self.set_secure_cookie('uid','',0)
        self.write('<h1>LogOut Success</h1>')
