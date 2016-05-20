import tornado.web
import tornado.gen
import datetime

from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

from Handlers.BaseHandler import BaseHandler
from Config.ParametersConfig import MID_THREAD_POOL_SIZE
from tools.dbtools import getQuerySQL,FetchAll,FetchOne
from tools.dbcore import ConnPool
from dao.statusdao import CheckContestIfAccept,CheckContestIfTry,CountContestACNum,CountContestSubmitNum

from UIModule.MsgModule import renderMSG


class ContestShowHandler(BaseHandler):
    executor = ThreadPoolExecutor(MID_THREAD_POOL_SIZE)

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        cid = self.get_argument('cid', None)

        uid = self.get_secure_cookie('uid',None)
        if uid is not None : uid = uid.decode()

        contestdetail = yield self.getContestsDetail(cid)
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cstatus = contestdetail[10]

        if cstatus == 0:
            self.write(renderMSG('Not Start'))
            self.finish()
            return

        rs,ac,totalsubmit,acsubmit,tr = yield self.getProblemList(cid,uid)
        print(contestdetail)

        self.render('contestshow.html',
                    begintime=contestdetail[5], endtime=contestdetail[6],
                    cstatus=contestdetail[10], ctitle=contestdetail[1],
                    now=now, rs=rs, cid=cid,ac=ac,totalsubmit=totalsubmit,acsubmit=acsubmit,tr=tr,
                    )

    def post(self):
        pass

    @run_on_executor
    def getContestsDetail(self, cid):
        wherecluse = ' cid = {} '.format(cid)
        ordclause = ' cid  '

        sql = getQuerySQL('contest', wherecluse, ordclause)
        rs = FetchOne(sql)


        return rs

    @run_on_executor
    def getProblemList(self, cid,uid):
        wherecluse = ' cid = {} '.format(cid)
        ordclause = ' cpid '

        sql = getQuerySQL(' cproblem ', wherecluse, ordclause)

        print(sql)
        rs = FetchAll(sql)

        ac = [ 0 for i in range(len(rs)) ]
        tr = [ 0 for i in range(len(rs)) ]

        for i in range(len(rs)) :
            if uid is not None :
                ac[i] = CheckContestIfAccept(uid,rs[i][2],cid)[0]
                if ac[i]==1: tr[i]=1
                else : tr[i] = CheckContestIfTry(uid,rs[i][2],cid)[0]


        totalsubmit = CountContestSubmitNum(cid)
        acsubmit = CountContestACNum(cid)

        td = dict()
        ad = dict()
        for x in totalsubmit: td[x[0]] = x[1]
        for x in acsubmit : ad[x[0]] = x[1]

        '''
        print(rs)
        print(ac)
        print(td)
        print(ad)
        '''

        return rs,ac,td,ad,tr
