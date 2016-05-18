import tornado.web

from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

from tools.dbcore import ConnPool
from tools.dbtools import getQuerySQL,getQueryDetailSQL,FetchAll,FetchOne
from tools.encode import Base64StrToUTF8Str

from Config.ParametersConfig import MID_THREAD_POOL_SIZE
from Handlers.BaseHandler import BaseHandler
from UIModule.MsgModule import renderMSG


class ShowCodeHandler(BaseHandler):
    executor = ThreadPoolExecutor(MID_THREAD_POOL_SIZE)

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        self.get_current_user()
        sid = self.get_argument('sid', -1)

        if sid == -1:
            self.write(renderMSG('wrong sid'))
            self.finish()
            return

        rs = yield self.getSubmitData(sid)


        isopen = int(rs[9])

        cid = int(rs[6])
        if cid == -1 :
            pass
        else :
            cstatus = yield self.getContestStatus(cid)
            if cstatus <= 1 : isopen = 0

        uid = int(rs[10])
        cookie_uid = self.get_secure_cookie('uid', None)
        if isopen == 0:
            if cookie_uid is None:
                pass
            elif int(cookie_uid) == uid:
                isopen = 1


        if isopen == 0:
            self.write(renderMSG('submit not public'))
            self.finish()
            return

        OJ = rs[12]
        Prob = rs[13]
        Code = Base64StrToUTF8Str(rs[8])
        Status = rs[2]
        Timesubmit = rs[1]
        PID = rs[5]
        Author = rs[11]
        language = rs[7]

        self.render('showcode.html', OJ=OJ, Prob=Prob, Code=Code, Status=Status,
                    Timesubmit=Timesubmit, PID=PID, Author=Author, language=language)

    def post(self):
        pass

    @run_on_executor
    def getSubmitData(self, sid):

        sql = getQuerySQL('status', ' sid = {} '.format(sid), ' sid ')
        rs = FetchOne(sql)

        return rs

    @run_on_executor
    def getContestStatus(self,cid):

        sql = getQueryDetailSQL(' contest ',' cstatus ',' cid = {} '.format(cid),' 1=1 ')
        rs = FetchOne(sql)

        return rs[0]

