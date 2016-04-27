from Handlers.BaseHandler import BaseHandler


class DebugHandler(BaseHandler):
    def get(self):
        self.render('webdebug.html')

    def post(self):
        id = self.get_argument("id", None)
        print('webdebug get id: ', id)
