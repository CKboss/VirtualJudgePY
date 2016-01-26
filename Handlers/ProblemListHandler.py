import tornado.web

import tornado.gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

from tools.dbtools import getPageLimitSQL
from tools.dbcore import conn

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
        index = self.get_argument('index','%')

        d = dict()

        if len(oj)==0 : oj='%'
        d['originOJ'] = oj
        if len(problem_id)==0 : problem_id='%'
        d['originProb'] = problem_id
        if len(problem_source)==0 : problem_source='%'
        d['source'] = problem_source
        if len(problem_title)==0 : problem_title='%'
        d['title'] = problem_title
        if len(index)==0 : index='%'

        print('oj:',oj,'problem_id:',problem_id,'problem_title:',problem_title,'problem_source:',problem_source,'index:',index)


        rs = yield self.getStauts(index,d)

        for r in rs :
            print(r)

        current_user = self.get_secure_cookie("username")
        if current_user is None : current_user = ''
        self.render("problemList.html",current_user=current_user,index=0,rs=rs)

    @run_on_executor
    def getStauts(self,index,data):
        # where clause

        whereclause = ''

        for key in data :
            if len(whereclause)!=0 :
                whereclause = whereclause + ' and '
            whereclause = whereclause + key + ' LIKE "%'+data[key]+'%"'

        ordclause = 'pid'

        if index != '%' and index != '0' : index=str(int(index)+19)
        else : index = '0'

        sql = getPageLimitSQL('problem',whereclause,ordclause,index,20)

        print(sql)

        cur = conn.cursor()
        cur.execute(sql)
        cur.close()

        rs = cur.fetchall()
        return rs


if __name__=='__main__':
    pass
