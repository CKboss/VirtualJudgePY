import requests
import time
import pickle
from queue import Queue

from Config.FilePathConfig import BZOJ_PKL_FILE
from bs4 import BeautifulSoup
from tools.RandA import RelUrlToAbsUrl

class BzojCrawler :

    base_url = 'http://www.lydsy.com/JudgeOnline/'
    prob_url = 'http://www.lydsy.com/JudgeOnline/problem.php?id={}'

    def CrawlerProblem(self,pid):

        url = self.prob_url.format(pid)

        r = requests.get(url)
        r.encoding = 'utf-8'

        '''
        f = open('/tmp/r2.html','w')
        f.write(r.text)
        f.close()
        '''

        html = r.text
        dt = self.getDetail(html)
        if dt is None :
            return

        dt['originOJ'] = 'BZOJ'
        dt['originProb'] = pid
        dt['url'] = url

        Term = ['description','input','output','sampleinput','sampleoutput','source','hint']

        for t in Term :
            dt[t] = RelUrlToAbsUrl(self.base_url,dt[t])


        path = BZOJ_PKL_FILE+'BZOJ_{}.pkl'.format(pid)
        f = open(path,'wb')
        pickle.dump(dt,f)

        print(str(pid)+' done !')

    def getDetail(self,html):
        dt = dict()

        soup = BeautifulSoup(html,'html5lib')

        # may be can't get
        Title =  soup.select_one('body > title').text
        if Title == 'Please contact lydsy2012@163.com!' :
            print('can\'t get problem')
            return None

        dt['title'] = soup.select_one('body > center:nth-of-type(3) > h2').text

        Terms = ['description','input','output','sampleinput','sampleoutput','hint','source'];

        for i in range(0,len(Terms)):
            item = Terms[i]
            dt[item] = soup.select_one('body > div:nth-of-type(%d)'%(i+1))
            if item == 'source' :
                dt[item] = soup.select_one('body > div:nth-of-type(%d)'%(i+1)).text

        limitinfo =  soup.select_one('body > center:nth-of-type(3)').text

        a1 = limitinfo.find('Time Limit:')
        a2 = limitinfo.find('Sec')

        b1 = limitinfo.find('Memory Limit:')
        b2 = limitinfo.find('MB')

        dt['timelimit'] = limitinfo[a1+11:a2+3]
        dt['memorylimit'] = limitinfo[b1+13:b2+2]

        p = limitinfo.find('Special Judge')

        if p == -1 :
            dt['specialjudge'] = 0
        else :
            dt['specialjudge'] = 1


        return dt

def crawlerFromTo(u,v) :

    bc = BzojCrawler()
    q = Queue()
    for x in range(u,v+1) :
        q.put(x)

    while q.empty() == False :
        pid = q.get()
        time.sleep(0.5)
        try :
            bc.CrawlerProblem(pid)
        except Exception as e :
            q.put(pid)
            print(pid,' error!!')

def main() :

    crawlerFromTo(1011,4012)

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

if __name__ == '__main__' :
    main()
