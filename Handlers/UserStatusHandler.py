import tornado.web
import tornado.gen
import urllib
import hashlib

from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

from Handlers.BaseHandler import BaseHandler
from tools.dbtools import getQuerySQL, getQueryDetailSQL, getUpdateSQL,FetchOne,FetchAll,ExeSQL
from tools.dbcore import ConnPool
from tools.encode import SHA512

from Config.ParametersConfig import MID_THREAD_POOL_SIZE
from UIModule.MsgModule import renderMSG

from dao.userdao import checkUserSQL
from dao.statusdao import GetUserRank


class UserStatusHander(BaseHandler):
    executor = ThreadPoolExecutor(MID_THREAD_POOL_SIZE)

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        username = self.get_argument('username')
        rs = yield self.getUserInfo(username)
        if rs is None:
            self.write(renderMSG('Can\'t find user {}'.format(username)))
            self.finish()

        uid = rs[0]
        nickname = rs[2]
        email = str(rs[4])
        school = rs[5]
        urlpart = hashlib.md5(email.lower().encode('utf-8')).hexdigest()

        rs = yield self.getUserACSubmit(username=username)

        rs2 = yield self.getSubmitInfo(uid=uid)

        rankinfo = yield self.getRankInfo(uname=username)
        '''
        submitdata = ''
        for x in rs2 :
            if len(submitdata) != 0 :
                submitdata += ',\n'
            submitdata += '{value:'+str(x[1])+',name:"'+str(x[0])+'"}'
        '''
        submitdata = rs2

        print(submitdata)

        self.render("userstatus.html", uid=uid, uname=username,nickname=nickname, email=email, school=school, urlpart=urlpart, rs=rs,
                    submitdata=submitdata,rank=rankinfo)

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):

        uid = self.get_argument('uid')
        username = self.get_argument('username')
        password = self.get_argument('password')
        newpassword = self.get_argument('newpassword')
        email = self.get_argument('email')
        school = self.get_argument('school')
        nickname = self.get_argument('nickname')

        # Check Password

        rs = yield self.CheckPasswrod(username=username, password=password)

        if rs[0] == 0:
            self.write(renderMSG('Wrong Password for user {}. Can\'t modify.'.format(username)))
            self.finish()

        # Update user Info
        data = dict()
        data['email'] = email
        data['school'] = school
        data['nickname'] = nickname

        if newpassword is not None and len(newpassword) != 0:
            data['password'] = SHA512(username+'@'+newpassword)

        isOK = yield self.UpdateUserInfo(uid=uid, data=data)

        if isOK == False:
            self.write(renderMSG('Update False!'))
        else:
            self.write(renderMSG('Update Success!'))

        self.finish()

    @run_on_executor
    def getUserInfo(self, username):

        if len(username) == 0:
            return None

        where = ' username = "{}" '.format(username)
        sql = getQuerySQL('user', whereclause=where, ordclause=' uid ')
        rs = FetchOne(sql)

        print(rs)

        return rs

    @run_on_executor
    def getUserACSubmit(self, username):

        where = 'username = "{}" and status LIKE "%Accept%"'.format(username)
        select = ' DISTINCT originOJ,originProb '
        sql = getQueryDetailSQL('status', selectitem=select, whereclause=where, ordclause=' originOJ,originProb ')

        print('sql: ', sql)
        rs = FetchAll(sql)

        return rs

    @run_on_executor
    def CheckPasswrod(self, username, password):

        sql = checkUserSQL(username=username, password=password)
        rs = FetchOne(sql)

        return rs

    @run_on_executor
    def UpdateUserInfo(self, uid, data):

        sql = getUpdateSQL('user', data=data, clause=' uid={} '.format(uid))

        print('sql: ', sql)

        try:
            ExeSQL(sql)
        except Exception:
            return False

        return True

    @run_on_executor
    def getSubmitInfo(self, uid):

        sql = 'SELECT status,count(status) from status WHERE uid = {} GROUP BY status ORDER BY status'.format(uid)
        rs = FetchAll(sql)

        return rs

    @run_on_executor
    def getRankInfo(self,uname):
        return GetUserRank(username=uname)
