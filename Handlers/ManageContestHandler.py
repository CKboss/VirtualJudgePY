import tornado.web
import tornado.gen

from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

from Handlers.BaseHandler import BaseHandler

from tools.dbcore import conn
from tools.dbtools import getQuerySQL
import datetime


class ManageContestHandler(BaseHandler) :

    executor = ThreadPoolExecutor(20)

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self, *args, **kwargs):

        action = self.get_argument('action')
        cid = self.get_argument('cid')

        if action == 'modify' :
            # modify contest
            rs = yield self.getContestDetail(cid)
            d1 = rs[5]
            d2 = rs[6]
            dt = d2-d1

            '''
            print(rs)
            print(d1.year,d1.month,d1.day,d1.hour,d1.minute)
            print(dt.days,dt.seconds)
            mm,ss = divmod(dt.seconds,60)
            hh,mm = divmod(mm,60)
            print(hh,mm,ss)
            '''

            lday = dt.days
            lmm,lss = divmod(dt.seconds,60)
            lhh,lmm = divmod(lmm,60)

            contesttype = int(rs[8])

            password = ''

            check1='checked'
            check2=''

            if contesttype == 1 :
                password = rs[4]
                check1 = ''
                check2 = "checked"

            ctitle = rs[1]
            cdescription = rs[2]


            self.render('contestdetail.html',
                        check1=check1,check2=check2,
                        ctitle=ctitle,cdescription=contesttype,
                        year=d1.year,month=d1.month,day=d1.day,hour=d1.hour,minute=d1.hour,
                        lday=lday,lhour=lhh,lminute=lmm,lsecond=lss,password=password)


        elif action == 'delete' :
            pass


    def post(self):
        pass


    @run_on_executor
    def getContestDetail(self,cid):

        whereclause = ' cid = {} '.format(cid)
        sql = getQuerySQL('contest',whereclause,' cid ')

        cur = conn.cursor()
        cur.execute(sql)
        rs = cur.fetchone()
        cur.close()

        return rs
