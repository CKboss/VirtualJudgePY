import tornado.web
from Handlers.BaseHandler import BaseHandler

class CreateContestHandler(BaseHandler):

    def get(self):
        self.get_current_user()
        if len(self.current_user) == 0 :
            self.write('<h1>Please LogIn First!!</h1>')
        self.write('<h1>CretateContestHandler</h1>')

    def post(self):
        pass
