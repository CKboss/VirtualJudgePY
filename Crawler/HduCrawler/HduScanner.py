import requests
import time
from bs4 import BeautifulSoup

from Crawler.HduCrawler.HduConfig import HduUser

class HduScanner :

    s = requests.session()
    scan_url = 'http://acm.hdu.edu.cn/status.php?first=&pid=&user={}&lang=0&status=0'

    def Analyse(self,html):
        '''
        f = open('/tmp/status.html','w')
        f.write(html)
        f.close()
        '''
        soup = BeautifulSoup(html,'html5lib')

        print('-'*30)

        for i in range(2,20):
            td = soup.select('#fixed_table > table > tbody > tr:nth-of-type({})'.format(i))
            if len(td) == 0 : break

            for con in td[0].contents :
                print(con.text)

        print('-'*30)


    def Scanner(self):

        while True:

            for x in HduUser :

                url = self.scan_url.format(x.get('username'))
                r = self.s.get(url)
                r.encoding = 'gb2312'
                self.Analyse(r.text)
                print('heihei')

            print('now wait')
            time.sleep(20)


if __name__=='__main__':
    hs = HduScanner()
    #hs.Scanner()
    f = open('/tmp/status.html','r')
    html = f.read()
    hs.Analyse(html)
