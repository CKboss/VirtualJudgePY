import tornado.web
import tornado.gen
import urllib
import hashlib

from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

from Handlers.BaseHandler import BaseHandler
from tools.dbtools import getQuerySQL,getQueryDetailSQL
from tools.dbcore import ConnPool

from Config.ParametersConfig import MID_THREAD_POOL_SIZE
from UIModule.MsgModule import renderMSG

class UserStatusHander(BaseHandler) :

    executor = ThreadPoolExecutor(MID_THREAD_POOL_SIZE)

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        username = self.get_argument('username')
        rs = yield self.getUserInfo(username)
        if rs is None :
            self.write(renderMSG('Can\'t find user {}'.format(username)))
            self.finish()

        uid = rs[0]
        email = str(rs[4])
        school = rs[5]
        urlpart = hashlib.md5(email.lower().encode('utf-8')).hexdigest()

        rs = yield self.getUserACSubmit(username)

        print(rs)

        self.render("userstatus.html",uid=uid,uname=username,email=email,school=school,urlpart=urlpart)

    @run_on_executor
    def getUserInfo(self,username):

        if len(username)==0 :
            return None

        where = ' username = "{}" '.format(username)
        sql = getQuerySQL('user',whereclause=where,ordclause=' uid ')

        conn = ConnPool.connect()
        cur = conn.cursor()
        cur.execute(sql)

        rs = cur.fetchone()

        cur.close()
        conn.close()

        return rs

    @run_on_executor
    def getUserACSubmit(self,username):

        where = 'username = "{}" and status LIKE "%Accept%"'.format(username)
        select = ' DISTINCT originOJ,originProb '
        sql = getQueryDetailSQL('status',selectitem=select,whereclause=where,ordclause=' originOJ,originProb ')

        print('sql: ',sql)

        conn = ConnPool.connect()
        cur = conn.cursor()
        cur.execute(sql)

        rs = cur.fetchall()

        cur.close()
        conn.close()

        return rs
