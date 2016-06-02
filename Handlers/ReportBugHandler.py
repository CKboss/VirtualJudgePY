
from Handlers.BaseHandler import BaseHandler

class ReportBugHandler(BaseHandler):

    def get(self):
        self.render("reportbug.html")

    def post(self, *args, **kwargs):
        pass
