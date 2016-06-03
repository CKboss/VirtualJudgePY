import tornado.web
import tornado.gen
import json
import time

from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

from Handlers.BaseHandler import BaseHandler
from Config.ParametersConfig import MID_THREAD_POOL_SIZE

from Crawler.BnuVJCrawler.BnuVJCrawler import BnuVJCrawler
from Crawler.HustCrawler.HustCrawler import HustCrawler
from UIModule.MsgModule import renderMSG

class CrawlerOnlineHandler(BaseHandler):

    executor = ThreadPoolExecutor(MID_THREAD_POOL_SIZE)

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        self.render('crawleronline.html')


    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):

        if self.request.files is not None:
            csv_meta = self.request.files
            content = csv_meta['csv'][0]['body'].decode()
            problemlist = content.split('\n')
            if len(problemlist) > 20 :
                self.write(renderMSG('Too many Problem to Crawler'))
                self.finish()
            else :
                nt = yield self.CrawlerCSV(problemlist)
                self.write(renderMSG('{} problem crawler success'.format(nt)))
                self.finish()
            return

        vj = self.get_argument('VJ',None)
        oj = self.get_argument('oj',None)
        prob = self.get_argument('prob',None)
        if oj is None or vj is None or prob is None or oj == 'ALL' :
            self.finish()
            return


        isok = yield self.CrawlerIt(vj,oj,prob)
        msg = renderMSG('Crawler Success! Visit <a href="/problem/{}/{}">here</a> enjoy it!'.format(oj,prob),waittime=1000000)
        self.write(msg)
        self.finish()

    @run_on_executor
    def CrawlerIt(self,vj,oj,prob):


        if vj == 'BNUVJ':
            if oj == 'ZOJ' : oj = 'ZJU'
            bvc = BnuVJCrawler()
            bvc.CrawlerProblem(originOJ=oj,originProb=prob)
        elif vj == 'HUST':
            huc = HustCrawler()
            huc.CrawlerProblem(oj,prob)

        time.sleep(3)
        return True

    @run_on_executor
    def CrawlerCSV(self,problemlist):
        nt=0
        for line in problemlist :
            item = line.split(',')
            if len(item) == 2 :
                oj = item[0]
                prob = item[1]
                if self.CrawlerIt('HUST',oj,prob) : nt+=1
            time.sleep(2)
        return nt
