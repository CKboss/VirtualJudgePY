import tornado.web
import tornado.gen
import time

from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

from Handlers.BaseHandler import BaseHandler
from Config.ParametersConfig import MID_THREAD_POOL_SIZE

from Crawler.BnuVJCrawler.BnuVJCrawler import BnuVJCrawler

class CrawlerOnlineHandler(BaseHandler):

    executor = ThreadPoolExecutor(MID_THREAD_POOL_SIZE)

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        self.render('crawleronline.html')


    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        oj = self.get_argument('oj',None)
        prob = self.get_argument('prob',None)
        if oj is None or prob is None or oj == 'ALL' :
            self.finish()
            return
        if oj == 'ZOJ' : oj = 'ZJU'
        isok = yield self.CrawlerIt(oj,prob)
        self.render('crawleronline.html')

    @run_on_executor
    def CrawlerIt(self,oj,prob):
        bvc = BnuVJCrawler()
        bvc.CrawlerProblem(originOJ=oj,originProb=prob)
        time.sleep(10)

