import requests
from bs4 import BeautifulSoup

from Crawler.PkuCrawler.PkuConfig import Pku_User


class PkuScanner:
    s = requests.session()

    scan_url = 'http://poj.org/status?problem_id=&user_id={}&result=&language='

    def Analyse(self, html):

        soup = BeautifulSoup(html, 'html5lib')

        L = list()

        for i in range(2, 30):

            td = soup.select_one('body > table.a > tbody > tr:nth-of-type({})'.format(i))

            if td is None: break

            dt = dict()
            dt['originOJ'] = 'PKU'

            titles = ['realrunid', 'nickname', 'originProb', 'status', 'runmemory',
                      'runtime', 'language', 'codelenth', 'realsubmittime']

            for con in td.contents:

                dt[titles[0]] = con.text
                if titles[0] == 'codelenth':
                    dt[titles[0]] = dt[titles[0]][:-1]
                titles = titles[1:]

            L.append(dt)

        return L

    def Scanner(self):

        L = list()

        for x in Pku_User:
            url = self.scan_url.format(x['user_id1'])
            r = self.s.get(url, timeout=5)

            '''
            f = open('/tmp/r1.text','w')
            f.write(r.text)
            f.close()
            '''

            tL = self.Analyse(r.text)

            L += tL

        return L


def main():
    PS = PkuScanner()

    print(PS.Scanner())

    '''
    f = open('/tmp/r2.html','r')
    html = f.read()
    L = PS.Analyse(html)
    print(L)
    '''


if __name__ == '__main__':
    main()
