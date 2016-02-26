import tornado.web
import tornado.gen

from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

from Handlers.BaseHandler import BaseHandler
from tools.dbcore import ConnPool
from tools.dbtools import getPageLimitSQL


class StatusHandler(BaseHandler):
    executor = ThreadPoolExecutor(4)

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):

        oj = self.get_argument('oj', '%')
        problem_id = str(self.get_argument('problem_id', '%')).replace(' ', '%')
        user_name = str(self.get_argument('user_name', '%')).replace(' ', '%')
        status = str(self.get_argument('status', '%')).replace(' ', '%')
        language = str(self.get_argument('language', '%')).replace(' ', '%')
        isSearch = self.get_argument('isSearch', None)
        index = str(self.get_argument('index', '0')).replace(' ', '%')
        cid = str(self.get_argument('cid', -1)).replace(' ', '%')

        if len(index) == 0:
            index = '0'

        if isSearch is not None:
            index = 0
            self.set_cookie('st_index', '0')
            self.set_cookie('st_problem_id', problem_id)
            self.set_cookie('st_language', language)
            self.set_cookie('st_status', status)
            self.set_cookie('st_oj', oj)
            self.set_cookie('st_username', user_name)

        d = dict()
        d['index'] = index
        d['originProb'] = problem_id
        d['language'] = language
        d['status'] = status
        d['username'] = user_name
        d['originOJ'] = oj
        d['cid'] = cid

        # print('isSearch:%s'%(isSearch))
        # print('oj:%s prob:%s username:%s status:%s language:%s'%(oj,problem_id,user_name,status,language))

        self.get_current_user()

        rs = yield self.getMsgs(d)

        hasNext = True

        print(len(rs))

        if len(rs) <= 20:
            hasNext = False
        else:
            rs = rs[:-1]

        self.render('status.html', rs=rs, hasNext=hasNext)

    @run_on_executor
    def getMsgs(self, Data):

        '''
        for key in Data :
            print(key,' ----> ',Data[key])
        '''

        wherecluse = ''

        for key in Data:
            if key == 'index':
                continue
            else:
                if len(wherecluse) != 0:
                    wherecluse += ' and '
                wherecluse += ' {} like "%{}%" '.format(key, Data[key])

        ordercluse = ' timesubmit desc '

        sql = getPageLimitSQL('status', wherecluse, ordercluse, Data['index'], 21)

        print(sql)
        conn = ConnPool.connect()
        cur = conn.cursor()
        cur.execute(sql)
        rs = cur.fetchall()

        cur.close()
        conn.close()

        return rs


def main():
    pass


if __name__ == '__main__':
    main()
