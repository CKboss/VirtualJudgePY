import tornado.web

import tornado.gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

from tools.dbtools import getPageLimitSQL
from tools.dbcore import ConnPool

class ProblemListHandler(tornado.web.RequestHandler) :

    executor = ThreadPoolExecutor(10)

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):

        #oj=&problem_id=&problem_title=&problem_source=

        oj = self.get_argument('oj','%')
        problem_id = self.get_argument('problem_id','%')
        problem_title = self.get_argument('problem_title','%')
        problem_source = self.get_argument('problem_source','%')

        issearch = self.get_argument('issearch',None)

        index = self.get_argument('index',None)

        if issearch is not None :

            oj = str(oj).replace(' ','%')
            problem_id = str(problem_id).replace(' ','%')
            problem_title = str(problem_title).replace(' ','%')
            problem_source = str(problem_source).replace(' ','%')

            # rember cookie
            index = 0 #to avoid delay
            self.set_cookie('pl_index','0')
            self.set_cookie('pl_oj',oj)
            self.set_cookie('pl_problem_id',problem_id)
            self.set_cookie('pl_problem_title',problem_title)
            self.set_cookie('pl_problem_source',problem_source)



        if index is None :
            index = self.get_cookie('pl_index',None)
            if index is None :
                self.set_cookie('pl_index','0')
                index = self.get_cookie('pl_index')

        print('the index: ',index)

        d = dict()

        if len(oj)==0 or oj=='ALL' : oj='%'
        d['originOJ'] = oj
        if len(problem_id)==0 : problem_id='%'
        d['originProb'] = problem_id
        if len(problem_source)==0 : problem_source='%'
        d['source'] = problem_source
        if len(problem_title)==0 : problem_title='%'
        d['title'] = problem_title

        print('oj:',oj,'problem_id:',problem_id,'problem_title:',problem_title,'problem_source:',problem_source,'index:',index)


        rs = yield self.getStauts(index,d)


        #for r in rs : print(r)

        current_user = self.get_secure_cookie("username")
        if current_user is None : current_user = ''

        hasNext = True
        if len(rs)==21 : rs = rs[:-1]
        else : hasNext = False

        #print(hasNext)

        self.render("problemList.html",current_user=current_user,rs=rs,hasNext=hasNext)

    @run_on_executor
    def getStauts(self,index,data):
        # where clause

        whereclause = ''

        for key in data :
            if len(whereclause)!=0 :
                whereclause = whereclause + ' and '
            whereclause = whereclause + key + ' LIKE "%'+data[key]+'%"'

        ordclause = 'originProb'

        if index == '%' : index='0'
        if index is None : index = '0'

        sql = getPageLimitSQL('problem',whereclause,ordclause,index,21)

        print(sql)
        conn = ConnPool.connect()
        cur = conn.cursor()
        cur.execute(sql)
        cur.close()
        conn.close()

        rs = cur.fetchall()

        print('rs size: ',len(rs))

        return rs


if __name__=='__main__':
    pass
