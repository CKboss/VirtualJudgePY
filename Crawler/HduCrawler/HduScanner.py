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

        #print('-'*30)

        L = list()

        for i in range(2,20):
            td = soup.select('#fixed_table > table > tbody > tr:nth-of-type({})'.format(i))
            if len(td) == 0 : break

            dt = dict()
            dt['originOJ'] = 'HDU'
            titles = ['realrunid','realsubmittime','result','originProb','runtime',
                      'runmemory','codelenth','language','nickname']
            for con in td[0].contents :
                dt[titles[0]] = con.text
                if titles[0] == 'codelenth' :
                    dt[titles[0]] = dt[titles[0]][:-1]
                titles = titles[1:]

            L.append(dt)

        return L


    def Scanner(self):

        L = list()

        for x in HduUser :

            url = self.scan_url.format(x.get('username'))
            r = self.s.get(url)
            r.encoding = 'gb2312'
            tL = self.Analyse(r.text)
            L += tL

        return L

    def UpdateToDB(self):
        pass

'''
def scann_test() :
    hs = HduScanner()
    hs.Scanner()

if __name__=='__main__':
    scann_test()
    f = open('/tmp/status.html','r')
    html = f.read()
    hs.Analyse(html)
'''
