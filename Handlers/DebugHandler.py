from Handlers.BaseHandler import BaseHandler

class DebugHandler(BaseHandler) :

    def get(self):
        self.render('webdebug.html')
