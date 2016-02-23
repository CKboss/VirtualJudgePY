import requests
import pickle
import time

from queue import Queue
from bs4 import BeautifulSoup

from Config.FilePathConfig import ZOJ_PKL_FILE
from tools.RandA import RelUrlToAbsUrl

class ZojCrawler() :

    base_url = 'http://acm.zju.edu.cn/onlinejudge/'
    prob_url = 'http://acm.zju.edu.cn/onlinejudge/showProblem.do?problemCode={}'

    def CrawlerProblem(self,pid):

        url = self.prob_url.format(pid)

        data = dict()
        data['originOJ'] = 'ZOJ'
        data['originProb'] = pid
        data['url'] = url

        r = requests.get(url)
        html = r.text
        soup = BeautifulSoup(html,'html5lib').select_one('#content')
        html = str(soup)

        '''
        f = open('/tmp/zoj3812.html','w')
        f.write(html)
        f.close()
        '''

        d = self.getDetail(html)

        for key in d :
            data[key] = d[key]

        Term = ['description','input','output','sampleinput','sampleoutput']

        for t in Term :
            if t not in data :
                continue
            data[t] = RelUrlToAbsUrl(self.base_url,data[t])

        f = open(ZOJ_PKL_FILE+'ZOJ_{}.pkl'.format(pid),'wb')

        pickle.dump(data,f)
        print(pid,' done!')

    def getDetail(self,html):

        dt = dict()

        soup = BeautifulSoup(html,'html5lib')

        #print(soup)

        title = soup.select_one('#content_body > center:nth-of-type(1) > span')
        dt['title'] = title.text

        limits = soup.select_one('#content_body > center:nth-of-type(2)')
        conts = str(limits.text)

        p1 = conts.find('Seconds')
        p2 = conts.find('KB')
        p3 = conts.find('Special Judge')

        s1 = 7
        s2 = 10

        while conts[p1-s1] != ' ':
            if s1 == 3 : break
            s1 -= 1

        while conts[p2-s2] != ' ':
            if s2 == 7 : break
            s2 -= 1


        dt['timelimit'] = conts[p1-s1:p1] + ' Seconds'
        dt['memorylimit'] = conts[p2-s2:p2] + ' KB'

        dt['description'] = soup.select_one('#content_body')

        if p3 != -1 : dt['specialjudge'] = 1
        else : dt['specialjudge'] = 0

        strong = soup.select('#content_body > strong')
        dt['source'] = strong[-1].text

        return dt

def crawlerFromTo(u,v) :

    zc = ZojCrawler()
    q = Queue()
    for x in range(u,v+1) :
        q.put(x)

    while q.empty() == False :
        pid = q.get()
        time.sleep(0.3)
        try :
            zc.CrawlerProblem(pid)
        except Exception :
            q.put(pid)
            print(pid,' error!!')


def main() :
    crawlerFromTo(1000,3900)


if __name__=='__main__':
    main()
