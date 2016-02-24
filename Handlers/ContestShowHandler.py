import tornado.web
import tornado.gen
import datetime

from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

from Handlers.BaseHandler import BaseHandler
from Config.ParametersConfig import MID_THREAD_POOL_SIZE
from tools.dbtools import getQuerySQL
from tools.dbcore import ConnPool

class ContestShowHandler(BaseHandler) :

    executor = ThreadPoolExecutor(MID_THREAD_POOL_SIZE)

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):

        cid = self.get_argument('cid',None)

        contestdetail = yield self.getContestsDetail(cid)
        rs = yield self.getProblemList(cid)
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(contestdetail)
        print(rs)

        self.render('contestshow.html',
                    begintime = contestdetail[5], endtime = contestdetail[6],
                    cstatus = contestdetail[10], ctitle = contestdetail[1],
                    now = now, rs = rs , cid = cid,
                    )

    def post(self):
        pass

    @run_on_executor
    def getContestsDetail(self,cid):

        wherecluse = ' cid = {} '.format(cid)
        ordclause = ' cid  '

        sql = getQuerySQL('contest',wherecluse,ordclause)

        conn = ConnPool.connect()
        cur = conn.cursor()
        cur.execute(sql)
        rs = cur.fetchone()
        cur.close()
        conn.close()

        return rs

    @run_on_executor
    def getProblemList(self,cid):

        wherecluse = ' cid = {} '.format(cid)
        ordclause = ' cpid '

        sql = getQuerySQL(' cproblem ',wherecluse,ordclause)

        print(sql)

        conn = ConnPool.connect()
        cur = conn.cursor()
        cur.execute(sql)
        conn.close()

        rs = cur.fetchall()

        cur.close()

        return rs

