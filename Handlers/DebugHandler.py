import tornado.web

class DebugHandler(tornado.web.RequestHandler) :

    def get(self):
        self.render('webdebug.html')
