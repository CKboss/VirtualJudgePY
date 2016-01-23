import tornado.web
import tornado.gen

from tools.dbcore import conn


from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

from Crawler.ProblemCrawler import HUSTProblemCralwer
from Crawler.HduCrawler.HduCrawler import HduCrawler

from tools.encode import UTF8StrToBase64Str,Base64StrToUTF8Str

class ProblemHandler(tornado.web.RequestHandler) :

    executor = ThreadPoolExecutor(4)

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self,oj=None,pid=None):
        print('oj: '+oj+' pid: '+pid)
        yield self.getProblem(oj,pid)
        self.render('problem.html')


    @run_on_executor
    def getProblem(self,oj,pid):

        pass
        '''
        cur = conn.cursor()
        row = cur.fetchone()

        if row is None :
            if oj.upper() == 'HDU' or oj.upper() == 'HDOJ' :
                crawler = HduCrawler()
                crawler.CrawlerProblem(pid)

            cur.execute(sql)
            row = cur.fetchone()
            print('now find it! ')

        Data = dict()

        Data['title'] = row[1]
        Data['description'] = Base64StrToUTF8Str(row[2])
        Data['input'] = Base64StrToUTF8Str(row[3])
        Data['output'] = Base64StrToUTF8Str(row[4])
        Data['sample_in'] = Base64StrToUTF8Str(row[5])
        Data['sample_out'] = Base64StrToUTF8Str(row[6])
        Data['source'] = Base64StrToUTF8Str(row[25])

        self.render('problem.html',Data=Data)
        '''

def main():
    pass

if __name__=='__main__':
    main()
