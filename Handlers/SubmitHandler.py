import tornado.gen
import tornado.web
import time
import pickle
import random
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

from Handlers.BaseHandler import BaseHandler
from Crawler.CrawlerConfig import AutoSubmit
from tools.dbtools import getInserSQL,LAST_INSERT_ID
from tools.encode import UTF8StrToBase64Str
from tools.dbcore import ConnPool

class SubmitHandler(BaseHandler):

    executor = ThreadPoolExecutor(10)

    def prepare(self):
        self.AS = AutoSubmit()

    def get(self, *args, **kwargs):

        cid = self.get_argument('cid',-1)
        OJ = self.get_argument('OJ',None)
        Prob = self.get_argument('Prob',None)
        pid = self.get_argument('pid',None)
        self.get_current_user()

        if OJ is None or Prob is None or pid is None:
            return

        ret = str(self.current_user)+OJ+Prob

        if len(self.current_user) == 0 :
            self.write('<h1>Please LogIn first!!!</h1>')
        else :
            self.render('submit.html',OJ=OJ,Prob=Prob,pid=pid,cid=cid)

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self, *args, **kwargs):

        self.get_current_user()
        pid = self.get_argument('pid',None)
        Prob = self.get_argument('Prob',None)
        lang = self.get_argument('language',None)
        code = self.get_argument('usercode',None)
        oj = self.get_argument('OJ',None)
        cid = self.get_argument('cid',-1)

        if lang is None or len(code)==0 or oj is None or code is None or pid is None :
            self.write('<h1>Submit Error!!</h1>')
        else :
            print('lang: ',lang,' oj: ',oj,' Prob: ',Prob,' code ',code,'user: ',self.current_user)
            yield self.SubmmitCollector(pid=pid,oj=oj,Prob=Prob,lang=lang,code=code,cid=cid)
            # insert into DB
            self.write('<h1>Submit Success!!</h1>')

        self.finish()

    @run_on_executor
    def SubmmitCollector(self,pid,oj,Prob,lang,code,cid):

        code = self.AddRandomSpace(code)

        self.AS.SubmmitSelector(oj=oj,prob=Prob,lang=lang,code=code)

        #Write Record into db
        self.InsertStatusToDB(pid=pid,oj=oj,Prob=Prob,lang=lang,code=code,cid=cid)


    def AddRandomSpace(self,code):
        # Add RandomSpace to avoid missjudge
        s = 'From VirtualJudge.PY '
        n = random.randint(1,50)
        code += '\n/*\n'
        for i in range(n) : code += s[i%21]
        code += '\n*/'
        return code

    def InsertStatusToDB(self,pid,oj,Prob,lang,code,cid):
        data = dict()

        data['pid'] = pid
        data['cid'] = cid
        data['language'] = lang
        data['originOJ'] = oj
        data['originProb'] = Prob
        data['source'] = UTF8StrToBase64Str(code)
        data['username'] = self.current_user
        data['uid']=str(self.get_secure_cookie('uid').decode('utf-8'))
        data['timesubmit'] = time.strftime('%Y-%m-%d %H:%M:%S')
        data['isdisplay'] = 1
        data['isopen'] = 1
        data['status'] = 'Pending'
        data['codelenth'] = str(len(code))

        sql = getInserSQL('status',data)

        conn = ConnPool.connect()
        cur = conn.cursor()
        cur.execute(sql)

        ''' create a pkl file'''
        file = '/home/ckboss/Desktop/Development/PKL/sid_{}.pkl'
        cur.execute(LAST_INSERT_ID())
        sid = cur.fetchone()[0]

        pkl = dict()
        pkl['sid'] = sid
        pkl['codelenth'] = data['codelenth']
        pkl['originOJ'] = data['originOJ']
        pkl['originProb'] = data['originProb']
        pkl['language'] = data['language']
        pkl['looplimit'] = 10

        fw = open(file.format(sid),'wb')
        pickle.dump(pkl,fw)

        cur.close()
        conn.close()

        print('status_sql: ',sql)
