import requests
import time
import pickle
import random
from queue import Queue

from Config.FilePathConfig import BZOJ_PKL_FILE
from bs4 import BeautifulSoup
from tools.RandA import RelUrlToAbsUrl,RelUrlToBase64Code

from Crawler.BzojCrawler.BzojConfig import Bzoj_LogIn_Url, BzojVIPUser


class BzojCrawler:
    base_url = 'http://www.lydsy.com/'
    prob_url = 'http://www.lydsy.com/JudgeOnline/problem.php?id={}'
    vips = None

    def CrawlerProblem(self, pid,vip=False):

        url = self.prob_url.format(pid)

        if vip == True:

            if self.vips is None :
                print('VIP user LOGIN')
                self.vips = requests.session()
                r = self.vips.post(url=Bzoj_LogIn_Url,data=random.choice(BzojVIPUser))

            r = self.vips.get(url,timeout=7)
            r.encoding = 'utf-8'
            html = r.text

            dt = self.getDetail(html)

            if dt is None:
                print(str(pid)+' can\'t get this problem ')
                return

            dt['originOJ'] = 'BZOJ'
            dt['originProb'] = pid
            dt['url'] = url

            Term = ['description', 'input', 'output', 'sampleinput', 'sampleoutput', 'source', 'hint']

            for t in Term:
                dt[t] = RelUrlToBase64Code(self.base_url, dt[t])

            path = BZOJ_PKL_FILE + 'BZOJ_{}.pkl'.format(pid)
            f = open(path, 'wb')
            pickle.dump(dt, f)

            print(str(pid) + ' done !')
            return


        r = requests.get(url, timeout=7)
        r.encoding = 'utf-8'

        '''
        f = open('/tmp/r2.html','w')
        f.write(r.text)
        f.close()
        '''

        html = r.text
        dt = self.getDetail(html)
        if dt is None:
            print(str(pid) + ' can\'t get problem')
            return

        dt['originOJ'] = 'BZOJ'
        dt['originProb'] = pid
        dt['url'] = url

        Term = ['description', 'input', 'output', 'sampleinput', 'sampleoutput', 'source', 'hint']

        for t in Term:
            dt[t] = RelUrlToAbsUrl(self.base_url, dt[t])

        path = BZOJ_PKL_FILE + 'BZOJ_{}.pkl'.format(pid)
        f = open(path, 'wb')
        pickle.dump(dt, f)

        print(str(pid) + ' done !')

    def getDetail(self, html):
        dt = dict()

        soup = BeautifulSoup(html, 'html5lib')

        # may be can't get
        Title = soup.select_one('body > title').text
        if Title == 'Please contact lydsy2012@163.com!':
            return None

        dt['title'] = soup.select_one('body > center:nth-of-type(3) > h2').text

        Terms = ['description', 'input', 'output', 'sampleinput', 'sampleoutput', 'hint', 'source'];

        for i in range(0, len(Terms)):
            item = Terms[i]
            dt[item] = soup.select_one('body > div:nth-of-type(%d)' % (i + 1))
            if item == 'source':
                dt[item] = soup.select_one('body > div:nth-of-type(%d)' % (i + 1)).text

        limitinfo = soup.select_one('body > center:nth-of-type(3)').text

        a1 = limitinfo.find('Time Limit:')
        a2 = limitinfo.find('Sec')

        b1 = limitinfo.find('Memory Limit:')
        b2 = limitinfo.find('MB')

        dt['timelimit'] = limitinfo[a1 + 11:a2 + 3]
        dt['memorylimit'] = limitinfo[b1 + 13:b2 + 2]

        p = limitinfo.find('Special Judge')

        if p == -1:
            dt['specialjudge'] = 0
        else:
            dt['specialjudge'] = 1

        return dt


def crawlerFromTo(u, v,vip=False):
    bc = BzojCrawler()
    q = Queue()
    for x in range(u, v + 1):
        q.put(x)

    while q.empty() == False:
        pid = q.get()
        time.sleep(10)
        try:
            if vip==False : bc.CrawlerProblem(pid)
            elif vip==True: bc.CrawlerProblem(pid,True)
        except Exception as e:
            print(e)
            q.put(pid)
            print(pid, ' error!!')


def main():
    crawlerFromTo(1000, 1002,True)

    '''
    BC = BzojCrawler()
    #BC.CrawlerProblem(2680)
    html = open('/tmp/r1.html','r').read()
    d = BC.getDetail(html)

    for key in d :
        print(key)
        print(d[key])
        print('\n'*2)
    '''


if __name__ == '__main__':
    main()
