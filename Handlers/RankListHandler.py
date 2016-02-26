import tornado.web
import tornado.gen
import datetime
import math

from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

from tools.dbtools import getQuerySQL, getQueryDetailSQL
from tools.dbcore import ConnPool

from Handlers.BaseHandler import BaseHandler
from Config.ParametersConfig import SML_THREAD_POOL_SIZE


class RankLishHandler(BaseHandler):
    executor = ThreadPoolExecutor(SML_THREAD_POOL_SIZE)

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):

        cid = self.get_argument('cid', -1)

        if cid == -1:
            self.write('wrong contest id')
            self.finish()

        contestInfo = yield self.getContestInfo(cid)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        statusdata = yield self.getStatusInfo(cid)
        problemlist = yield self.getProblemList(cid)
        begintime = contestInfo[5]
        ranklist = yield self.CaluRankList(begintime, statusdata, problemlist)

        self.render('ranklist.html',
                    ctitle=contestInfo[1], begintime=contestInfo[5], endtime=contestInfo[6],
                    now=str(now), cstatus=contestInfo[10], cid=cid, ranklist=ranklist
                    )

    def post(self):
        pass

    @run_on_executor
    def CaluRankList(self, begintime, statusdata, problemlist):

        '''
        print('status data: ')
        print(statusdata)
        print('problem list : ')
        print(problemlist)
        '''

        begintime = datetime.datetime.strptime(str(begintime), '%Y-%m-%d %H:%M:%S')

        np = len(problemlist)

        if np == 0:
            return tuple()

        mincpi = int(problemlist[0][0])

        pInC = dict()
        for prob in problemlist:
            pInC[prob[1]] = int(prob[0]) - mincpi

        userList = list()

        for x in statusdata:

            uid = x[10]
            username = x[11]

            dt = dict()
            dt['uid'] = uid
            dt['username'] = username

            # 初始化AC数组和罚时数组
            dt['aclist'] = [0 for row in range(np)]
            dt['ptimelist'] = [0 for row in range(np)]
            dt['submit'] = [0 for row in range(np)]
            dt['totalaccept'] = 0
            dt['totaltime'] = 0

            if dt not in userList:
                # print(dt)
                userList.append(dt)

        ranklist = list()
        for user in userList:

            for status in statusdata:
                if status[10] == user['uid'] and status[11] == user['username']:

                    pid = status[5]

                    id = pInC[pid]

                    # 已经ac不计算之后的提交
                    if user['aclist'][id] == 1: continue

                    result = str(status[2]).strip().lower()
                    user['submit'][id] += 1

                    if result == 'accept' or result == 'accepted':
                        # ac 标记该题已经ac

                        user['aclist'][id] = 1

                        timesubmit = status[1]
                        timesubmit = datetime.datetime.strptime(str(timesubmit), '%Y-%m-%d %H:%M:%S')
                        deta = timesubmit - begintime

                        user['ptimelist'][id] += deta.total_seconds()
                    else:
                        # 没有ac加上罚时间20*60s
                        user['ptimelist'][id] += 1200

            # 统计总罚时和ac数
            for i in range(0, np):
                if user['aclist'][i] == 1:
                    user['totalaccept'] += 1
                    user['totaltime'] += user['ptimelist'][i]

            ranklist.append(user)
            # print('user: ',user)
            # print('\n')

        ranklist = sorted(ranklist, key=lambda user: user['totalaccept'] * 1000000000000 - user['totaltime'])

        return ranklist

    @run_on_executor
    def getContestInfo(self, cid):

        whereclause = ' cid = {} '.format(cid)

        sql = getQuerySQL('contest', whereclause=whereclause, ordclause=' cid ')

        conn = ConnPool.connect()
        cur = conn.cursor()
        cur.execute(sql)
        rs = cur.fetchone()
        cur.close()
        conn.close()

        return rs

    @run_on_executor
    def getStatusInfo(self, cid):

        whereclause = ' cid = {} '.format(cid)
        ordclause = ' sid '

        sql = getQuerySQL('status', whereclause=whereclause, ordclause=ordclause)

        conn = ConnPool.connect()
        cur = conn.cursor()
        cur.execute(sql)
        rs = cur.fetchall()
        cur.close()
        conn.close()

        return rs

    @run_on_executor
    def getProblemList(self, cid):

        whereclause = ' cid = {} '.format(cid)
        ordclause = ' cpid '
        selectitem = ' cpid,pid '

        sql = getQueryDetailSQL('cproblem', selectitem=selectitem, whereclause=whereclause, ordclause=ordclause)

        conn = ConnPool.connect()
        cur = conn.cursor()
        cur.execute(sql)
        rs = cur.fetchall()
        cur.close()
        conn.close()

        return rs
