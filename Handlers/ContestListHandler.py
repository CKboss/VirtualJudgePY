import tornado.web
import tornado.gen

from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

from Handlers.BaseHandler import BaseHandler
from tools.dbtools import getPageLimitSQL, getQueryDetailSQL
from tools.dbcore import ConnPool
from Config.ParametersConfig import BIG_THREAD_POOL_SIZE, PAGE_LIMIT


class ContestListHandler(BaseHandler):
    executor = ThreadPoolExecutor(BIG_THREAD_POOL_SIZE)

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):

        page = self.get_argument('page', 0)
        rs = yield self.getContestsDetail(page)

        hasNext = True

        if len(rs) != PAGE_LIMIT + 1:
            hasNext = False
        else:
            rs = rs[:-1]

        self.render('contestlist.html',
                    rs=rs, hasNext=hasNext, page=page
                    )

    def post(self):
        pass

    @run_on_executor
    def getContestsDetail(self, page):

        From = int(page) * PAGE_LIMIT

        sql = 'SELECT *,(SELECT username FROM user WHERE uid = contest.cuid) as username FROM contest ORDER BY contest.cid DESC LIMIT {} , {} '.format(
            From, PAGE_LIMIT + 1)

        print(sql)

        conn = ConnPool.connect()
        cur = conn.cursor()
        cur.execute(sql)
        rs = cur.fetchall()
        cur.close()
        conn.close()

        return rs
