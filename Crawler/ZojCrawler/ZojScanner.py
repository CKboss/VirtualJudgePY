import requests
from bs4 import BeautifulSoup

from Crawler.ZojCrawler.ZojConfig import Zoj_User


class ZojScanner:
    s = requests.session()

    scan_url = 'http://acm.zju.edu.cn/onlinejudge/showRuns.do?contestId=1&search=true&firstId=-1&lastId=-1&problemCode=&handle={}&idStart=&idEnd='

    def Analyse(self, html):

        soup = BeautifulSoup(html, 'html5lib')
        L = list()

        for i in range(2, 30):

            tr = soup.select_one('#SubmissionSearchForm > table > tbody > tr:nth-of-type({})'.format(i))
            if tr is None: break

            dt = dict()
            dt['originOJ'] = 'ZOJ'

            titles = ['realrunid', 'realsubmittime', 'status', 'originProb', 'language'
                , 'runtime', 'runmemory', 'nickname']

            for con in tr.contents:
                try:
                    dt[titles[0]] = con.text.strip()
                    titles = titles[1:]
                except Exception:
                    pass

            L.append(dt)

        return L

    def Scanner(self):

        L = list()

        for x in Zoj_User:
            url = self.scan_url.format(x['handle'])
            r = self.s.get(url, timeout=5)

            '''
            f = open('/tmp/R2.html','w')
            f.write(r.text)
            f.close()
            '''

            tl = self.Analyse(r.text)

            L += tl

        return L


def main():
    ZS = ZojScanner()
    L = ZS.Scanner()
    for x in L:
        print(x)
    '''
    f = open('/tmp/R2.html','r')
    html = f.read()
    L = ZS.Analyse(html)
    print(L)
    '''


if __name__ == '__main__':
    main()
