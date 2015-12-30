import tornado.web

class IndexHandler(tornado.web.RequestHandler) :

    def get(self):

        name = self.get_secure_cookie("username")

        if name is None :
            name=''

        self.render('index.html',name=name)
