import tornado.web
import tornado.gen

from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

from Config.ParametersConfig import MID_THREAD_POOL_SIZE
from Config.ParametersConfig import PAGE_LIMIT

from Handlers.BaseHandler import BaseHandler
from dao.statusdao import GetAuthorsRank

class AuthorsRanklistHandler(BaseHandler):

    executor = ThreadPoolExecutor(MID_THREAD_POOL_SIZE)

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):

        page = self.get_argument('page',0)
        page = int(page)
        if page < 0 : page = 0

        rs = yield self.getRankList(page=page,pagelimit=PAGE_LIMIT)
        hasnext = True

        if len(rs) == PAGE_LIMIT+1 : rs = rs[:-1]
        else : hasnext = False

        print('page: ',page,type(page))
        self.render('authorsranklist.html',
                    rs=rs,hasNext=hasnext,page=page,prepage=page-1,nxtpage=page+1)


    @run_on_executor
    def getRankList(self,page,pagelimit):
        rs = GetAuthorsRank(page,pagelimit)
        print(rs)
        return rs
