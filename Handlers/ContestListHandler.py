import tornado.web
from Handlers.BaseHandler import BaseHandler

class ContestListHandler(BaseHandler) :

    def get(self):
        self.render('contestlist.html')

    def post(self):
        pass
