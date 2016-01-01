import tornado.web

class LogOutHandler(tornado.web.RequestHandler) :

    def post(self, *args, **kwargs):
        self.set_secure_cookie("username",'',0)
        self.redirect("/")
