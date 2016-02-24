import tornado.web
import tornado.gen
import datetime
import math

from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

from tools.dbtools import getQuerySQL,getQueryDetailSQL
from tools.dbcore import ConnPool

from Handlers.BaseHandler import BaseHandler
from Config.ParametersConfig import SML_THREAD_POOL_SIZE

class RankLishHandler(BaseHandler) :

    executor = ThreadPoolExecutor(SML_THREAD_POOL_SIZE)

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):

        cid = self.get_argument('cid',-1)

        if cid == -1:
            self.write('wrong contest id')
            self.finish()

        contestInfo = yield self.getContestInfo(cid)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        statusdata = yield self.getStatusInfo(cid)
        problemlist = yield self.getProblemList(cid)
        ranklist = yield self.CaluRankList(statusdata,problemlist)

        self.render('ranklist.html',
                    ctitle=contestInfo[1],begintime = contestInfo[5],endtime = contestInfo[6],
                    now = str(now), cstatus = contestInfo[10],cid = cid,
                    )

    def post(self):
        pass

    @run_on_executor
    def CaluRankList(self,statusdata,problemlist):

        print(statusdata)
        print(problemlist)

        mincpi = 99999999999999
        np = len(problemlist)

        for prob in problemlist :
            mincpi = min(mincpi,int(prob[0]))

        userList = list()

        for x in statusdata :

            uid = x[10]
            username = x[11]

            dt = dict()
            dt['uid'] = uid
            dt['username'] = username

            if dt not in userList :
                userList.append(dt)

        for user in userList :

            for status in statusdata :
                if status[10] == user['uid'] and status[11] == user['username'] :

                    pass

        ranklist = list()

        return ranklist


    @run_on_executor
    def getContestInfo(self,cid):

        whereclause = ' cid = {} '.format(cid)

        sql = getQuerySQL('contest',whereclause=whereclause,ordclause=' cid ')

        conn = ConnPool.connect()
        cur = conn.cursor()
        cur.execute(sql)
        rs = cur.fetchone()
        cur.close()
        conn.close()

        return rs

    @run_on_executor
    def getStatusInfo(self,cid):

        whereclause = ' cid = {} '.format(cid)
        ordclause = ' sid '

        sql = getQuerySQL('status',whereclause=whereclause,ordclause=ordclause)

        conn = ConnPool.connect()
        cur = conn.cursor()
        cur.execute(sql)
        rs = cur.fetchall()
        cur.close()
        conn.close()

        return rs

    @run_on_executor
    def getProblemList(self,cid):

        whereclause = ' cid = {} '.format(cid)
        ordclause = ' cpid '
        selectitem = ' pid '

        sql = getQueryDetailSQL('cproblem',selectitem=selectitem,whereclause=whereclause,ordclause=ordclause)

        conn = ConnPool.connect()
        cur = conn.cursor()
        cur.execute(sql)
        rs = cur.fetchall()
        cur.close()
        conn.close()

        return rs


