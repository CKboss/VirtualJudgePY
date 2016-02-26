import tornado.web
import tornado.gen
import datetime
import pickle

from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

from tools.dbcore import ConnPool
from tools.dbtools import getInserSQL, LAST_INSERT_ID

from Handlers.BaseHandler import BaseHandler
from Config.FilePathConfig import PendingContestFile


class CreateContestHandler(BaseHandler):
    executor = ThreadPoolExecutor(10)

    def get(self):
        self.get_current_user()
        if len(self.current_user) == 0:
            self.write('<h1>Please LogIn First!!</h1>')
            return
        now = datetime.datetime.now()
        now = now + datetime.timedelta(minutes=10)

        self.render('createcontest.html', year=now.year, hour=now.hour, month=now.month, day=now.day, minute=now.minute)

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):

        self.get_current_user()
        if len(self.current_user) == 0:
            self.write('<h1>Please LogIn First!!</h1>')
            self.finish()
            return

        d = self.request.arguments
        for x in d: d[x] = d[x][0].decode()

        if self.check_args(d) == False:
            self.write('create fail some arguments miss')
            self.finish()
            return

        uid = self.get_secure_cookie('uid').decode()
        data = self.getContestData(uid, d)

        if 'error' in data:
            self.write(data['error'])
            self.finish()
            return

        cid = yield self.CreateNewContest(data)

        self.MakePendingContestTempFile(cid, data)

        self.write('create success !!')
        self.finish()

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
    def CreateNewContest(self, data):

        sql = getInserSQL('contest', data)

        print('exeSQL: Create Contest!! ', sql)
        conn = ConnPool.connect()
        cur = conn.cursor()
        cur.execute(sql)

        sql = LAST_INSERT_ID()
        cur.execute(sql)
        id = cur.fetchone()[0]

        cur.close()
        conn.close()

        return id
