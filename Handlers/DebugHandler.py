from Handlers.BaseHandler import BaseHandler
from Crawler.HustCrawler.HustConfig import HustUser

class DebugHandler(BaseHandler):
    def get(self):
        self.render('webdebug.html')

    def post(self):
        id = self.get_argument("id", None)
        print('webdebug get id: ', id)

if __name__=='__main__':
    print('hi')
