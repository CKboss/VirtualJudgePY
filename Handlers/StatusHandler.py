import tornado.web
import tornado.gen

from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

from Crawler.ResultCrawler import HUSTResualtCrawler

class StatusHandler(tornado.web.RequestHandler):

    executor = ThreadPoolExecutor(4)

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        #msgs = yield self.getMsgs()
        name = self.get_secure_cookie('username')
        if name is None : name=''
        self.render('status.html',current_user=name)

    @run_on_executor
    def getMsgs(self):
        return HUSTResualtCrawler().getResult()


def main():
    pass

if __name__=='__main__':
    main()
