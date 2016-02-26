from Handlers.BaseHandler import BaseHandler


class IndexHandler(BaseHandler):
    def get(self):
        name = self.get_secure_cookie('username')
        if name is None: name = ''

        self.render('index.html', current_user=name)
