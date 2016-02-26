import requests
from bs4 import BeautifulSoup

from Crawler.BzojCrawler.BzojConfig import BzojUser

class BzojScanner :

    s = requests.session()
    scan_url = 'http://www.lydsy.com/JudgeOnline/status.php?problem_id=&user_id={}&language=-1&jresult=-1'

    def Analyse(self,html):

        soup = BeautifulSoup(html,'html5lib')

        L =list()

        for i in range(2,30) :

            html = soup.select_one('body > center:nth-of-type(1) > table:nth-of-type(2) > tbody > tr:nth-of-type({})'.format(i))
            if html is None : break

            dt = dict()
            dt['originOJ'] = 'BZOJ'
            Term = ['','realrunid','nickname','originProb','status','runmemory','runtime','language','codelenth','timesubmit']
            for j in range(1,10) :
                html = soup.select_one('body > center:nth-of-type(1) > table:nth-of-type(2) > tbody > tr:nth-of-type({}) > td:nth-of-type({})'.format(i,j))
                dt[Term[j]] = html.text
                if Term[j] == 'codelenth' :
                    dt[Term[j]] = str(dt[Term[j]]).replace(' B','')

            L.append(dt)

        return L


    def Scanner(self):

        L = list()

        for x in BzojUser :

            url = self.scan_url.format(x['user_id'])
            r = self.s.get(url,timeout=5)
            r.encoding = 'utf-8'

            html = r.text
            tL = self.Analyse(html)

            L+=tL

        return L


def main() :
    bs = BzojScanner()
    L = bs.Scanner()
    print(L)
    '''
    f = open('/tmp/hi.html','r')
    html = f.read()
    tL = bs.Analyse(html)
    print(tL)
    '''

if __name__=='__main__' :
    main()
