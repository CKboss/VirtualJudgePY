import tornado.web
import tornado.gen

from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

from tools.dbtools import getPageLimitSQL,ExeSQL,FetchAll
from tools.dbcore import ConnPool

from Handlers.BaseHandler import BaseHandler
from UIModule.MsgModule import renderMSG


class ManageContestListHandler(BaseHandler):
    executor = ThreadPoolExecutor(20)

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self, *args, **kwargs):
        self.get_current_user()

        if len(self.current_user) == 0:
            self.write(renderMSG('please log in first !!'))
            self.finish()
            return

        uid = self.get_secure_cookie('uid').decode()

        rs = yield self.getContests(uid)

        self.render('managecontestlist.html', rs=rs)

    @run_on_executor
    def getContests(self, uid):
        whereclause = ' cuid = {}'.format(uid)
        ordclause = ' cid desc '

        sql = getPageLimitSQL('contest', whereclause, ordclause, 0, 100000)
        rs = FetchAll(sql)

        return rs
