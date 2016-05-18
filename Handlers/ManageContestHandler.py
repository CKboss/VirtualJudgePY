import tornado.web
import tornado.gen

from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

from Handlers.BaseHandler import BaseHandler

from tools.dbcore import ConnPool
from tools.dbtools import getQueryDetailSQL, getDeletSQL, getInserSQL, getQuerySQL, getUpdateSQL,FetchAll,FetchOne,ExeSQL
from Config.FilePathConfig import PendingContestFile
from UIModule.MsgModule import renderMSG

import pickle
import datetime


class ManageContestHandler(BaseHandler):
    executor = ThreadPoolExecutor(20)

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self, *args, **kwargs):

        action = self.get_argument('action')
        cid = self.get_argument('cid')

        if action == 'modify':
            # modify contest
            rs = yield self.getContestDetail(cid)
            d1 = rs[5]
            d2 = rs[6]
            dt = d2 - d1

            '''
            print(rs)
            print(d1.year,d1.month,d1.day,d1.hour,d1.minute)
            print(dt.days,dt.seconds)
            mm,ss = divmod(dt.seconds,60)
            hh,mm = divmod(mm,60)
            print(hh,mm,ss)
            '''

            lday = dt.days
            lmm, lss = divmod(dt.seconds, 60)
            lhh, lmm = divmod(lmm, 60)

            contesttype = int(rs[8])

            password = ''

            check1 = 'checked'
            check2 = ''

            if contesttype == 1:
                password = rs[4]
                check1 = ''
                check2 = "checked"

            ctitle = rs[1]
            cdescription = rs[2]

            problemlist = yield self.getContestProblem(cid)
            problemlisttxt = self.getProblemTxt(problemlist)

            self.render('contestdetail.html',
                        cid=cid,
                        check1=check1, check2=check2,
                        ctitle=ctitle, cdescription=cdescription,
                        year=d1.year, month=d1.month, day=d1.day, hour=d1.hour, minute=d1.minute,
                        lday=lday, lhour=lhh, lminute=lmm, lsecond=lss, password=password,
                        problemlist=problemlist, problemlisttxt=problemlisttxt
                        )


        elif action == 'delete':

            if cid is None:
                self.write(renderMSG('Wrong CID'))
                self.finish()
                return

            flag = yield  self.DeleteContest(cid)

            if flag == True :
                self.write(renderMSG('Delete Success!'))
            else :
                self.write(renderMSG('Can\'t delete'))

            self.finish()

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):

        action = self.get_argument('action', None)

        if action is None:
            self.write(renderMSG('Error Manage Operation!!'))
            self.finish()
            return

        if action == 'updateproblem':

            cid = self.get_argument('cid', None)
            txt = self.get_argument('problemlist', None)

            if cid is None:
                self.write(renderMSG('Wrong CID'))
                self.finish()
                return

            CD = yield self.getContestDetail(cid)
            cstatus = CD[10]

            if cstatus == 1 or cstatus == 2:
                self.write(renderMSG('Contest is frost can\'t modify'))
                self.finish()
                return

            problemlist = self.getProblem(txt)

            log = yield self.UpdateProblem(cid, problemlist)

            self.write(renderMSG(log))
            self.finish()
            return

        elif action == 'updatedetail':

            d = self.request.arguments
            for x in d: d[x] = d[x][0].decode()
            cid = d['cid']

            if self.check_args(d) == False:
                self.write(renderMSG('create fail some arguments miss'))
                self.finish()
                return

            uid = self.get_secure_cookie('uid').decode()
            data = self.getContestData(uid, d)

            if 'error' in data:
                self.write(renderMSG(data['error']))
                self.finish()
                return

            CD = yield self.getContestDetail(cid)
            cstatus = CD[10]

            if cstatus == 1 or cstatus == 2:
                self.write(renderMSG('Contest is frost can\'t modify'))
                self.finish()
                return

            yield self.updateContestDetail(cid, data)
            self.MakePendingContestTempFile(cid, data)

            self.write(renderMSG('Update Success'))
            self.finish()
            return

        elif action=='delete' :
            cid = self.get_argument('cid', None)

            if cid is None:
                self.write(renderMSG('Wrong CID'))
                self.finish()
                return

            yield  self.DeleteContest(cid)

            self.write(renderMSG('Delete Success!'))
            self.finish()

    def check_args(self, d):
        L = ['contestname', 'syear', 'smonth', 'sday', 'shour',
             'sminute', 'ssecond', 'lday', 'lhour', 'lminute',
             'lsecond', 'contesttype', 'password', 'hide']
        for x in L:
            if x not in d: continue
            if len(d[x]) == 0:
                if x == 'password' and d['contesttype'] == '0':
                    continue
                return False
        return True

    def getContestData(self, uid, d):

        data = dict()
        data['cuid'] = uid
        data['ctitle'] = d['contestname']

        if 'contesttype' not in d or len(d['contesttype']) == 0:
            data['ispublic'] = "0"

        data['ispublic'] = d['contesttype']

        print(data['ispublic'])
        if data['ispublic'] == "1":
            data['password'] = d['password']

        data['cdescription'] = d['cdescription']

        d1 = datetime.datetime(int(d['syear']), int(d['smonth']), int(d['sday']), int(d['shour']), int(d['sminute']))
        dt = datetime.timedelta(days=int(d['lday']), hours=int(d['lhour']), minutes=int(d['lminute']));

        now = datetime.datetime.now()

        if (d1 - now).total_seconds() < 0:
            data['error'] = 'wrong begin time'
        if dt.total_seconds() > 2700000:
            data['error'] = 'to long'

        d2 = d1 + dt

        data['begintime'] = str(d1)
        data['endtime'] = str(d2)
        data['cstatus'] = 0

        return data

    @run_on_executor
    def updateContestDetail(self, cid, data):

        wherecluse = ' cid = {} '.format(cid)
        sql = getUpdateSQL('contest', data, wherecluse)
        print(sql)
        ExeSQL(sql)


    def MakePendingContestTempFile(self, cid, data):

        file = open(PendingContestFile + '/contest_' + str(cid) + '.pkl', 'wb')

        dt = dict()
        dt['cid'] = cid
        dt['ctitle'] = data['ctitle']
        dt['begintime'] = data['begintime']
        dt['endtime'] = data['endtime']
        dt['cstatus'] = data['cstatus']
        dt['submitlist'] = list()
        dt['ranklist'] = list()

        pickle.dump(dt, file)

    def getProblem(self, txt):

        Li = txt.split('\r\n')
        data = list()
        for item in Li:
            di = dict()
            ii = item.split(' ')
            if len(ii) == 2:
                di['originOJ'] = ii[0]
                di['originProb'] = ii[1]
                if di not in data:
                    data.append(di)

        return data

    def getProblemTxt(self, list):
        ret = ''
        for x in list:
            ret += x[4] + ' ' + x[5] + '\n'
        return ret

    @run_on_executor
    def getContestDetail(self, cid):

        whereclause = ' cid = {} '.format(cid)
        sql = getQuerySQL('contest', whereclause, ' cid ')
        rs = FetchOne(sql)

        return rs

    @run_on_executor
    def getContestProblem(self, cid):

        whereclause = ' cid = {} '.format(cid)
        sql = getQuerySQL('cproblem', whereclause, ' cpid ')
        rs = FetchAll(sql)

        return rs

    @run_on_executor
    def UpdateProblem(self, cid, data):

        # clear old problem in contest

        whereclause = ' cid = {} '.format(cid)
        sql = getDeletSQL('cproblem', whereclause)

        conn = ConnPool.connect()
        cur = conn.cursor()
        cur.execute(sql)

        log = ''

        for item in data:

            # get pid
            whereclause = ' originOJ = "{originOJ}" and originProb = "{originProb}" '.format(**item)
            sql = getQueryDetailSQL('problem', '*', whereclause, ' pid ')
            num = cur.execute(sql)

            if num == 0:
                log += 'Error when add Problem OJ: {originOJ} Pid: {originProb}<br>'.format(**item)
                log += '\n'
            else:

                rs = cur.fetchone()
                pid = rs[0]
                title = rs[1]
                originOJ = rs[4]
                originProb = rs[5]

                # insert into cproblem

                data = dict()
                data['cid'] = cid
                data['pid'] = pid
                data['title'] = title
                data['originOJ'] = originOJ
                data['originProb'] = originProb

                sql = getInserSQL('cproblem', data)
                cur.execute(sql)

        cur.close()
        conn.close()

        if len(log) == 0:
            log += 'All problem add into contest {} successfully. <br>'.format(cid)
        else:
            log += 'some error happend.<br> May be some problem can\'t find this problem in database...<br>'

        return log

    @run_on_executor
    def DeleteContest(self,cid):

        whereclause = ' cid = {} '.format(cid)

        conn = ConnPool.connect()
        cur = conn.cursor()

        sql = getQueryDetailSQL('contest',' cstatus ',whereclause,'1=1')
        cur.execute(sql)
        r = cur.fetchone()

        if r[0] != 0 :
            return False


        sql = getDeletSQL('cproblem', whereclause)

        cur.execute(sql)
        sql = getDeletSQL('contest',whereclause=whereclause)

        cur.execute(sql)


        sql = getDeletSQL('contest', whereclause)

        cur.execute(sql)
        cur.close()

        return True