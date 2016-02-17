import requests
import pickle
import time
from queue import Queue
from bs4 import BeautifulSoup

from tools.RandA import RelUrlToAbsUrl

class PkuCrawler() :

    base_url = 'http://poj.org/'
    prob_url = 'http://poj.org/problem?id='

    def CrawlerProblem(self,pid):

        url = self.prob_url+str(pid)

        data = dict()
        data['originOJ'] = 'PKU'
        data['originProb'] = pid
        data['url'] = url

        r = requests.get(url)
        html = r.text
        soup = BeautifulSoup(html,'html5lib').select_one('body > table:nth-of-type(2)')
        html = str(soup)

        d = self.getDetail(html)

        for key in d :
            data[key] = d[key]

        Term = ['description','input','output','sampleinput','sampleoutput']

        for t in Term :
            data[t] = RelUrlToAbsUrl(self.base_url,data[t])

        f = open('/home/ckboss/Desktop/Development/testData/POJ/POJ_%04d.pkl'%pid,'wb')

        pickle.dump(data,f)
        print(pid,' done!')

    def getDetail(self,html):

        d = dict()

        soup = BeautifulSoup(html,'html5lib')
        d['title'] = soup.select_one('body > table > tbody > tr > td > div.ptt').text

        id = 4
        for key in ['description','input','output','source'] :
            d[key] = soup.select_one('body > table > tbody > tr > td > div:nth-of-type({})'.format(id))
            id+=1
        content = soup.find_all('pre',class_='sio')

        d['sampleinput'] = content[0]
        d['sampleoutput'] = content[1]
        d['source'] = BeautifulSoup(str(d['source']),'html5lib').text

        ''' get limit info'''

        d['timelimit'] = soup.select_one('body > table > tbody > tr > td > div.plm > table > tbody > tr:nth-of-type(1) > td:nth-of-type(1)').text.replace('Time Limit:','')
        d['memorylimit'] = soup.select_one('body > table > tbody > tr > td > div.plm > table > tbody > tr:nth-of-type(1) > td:nth-of-type(3)').text.replace('Memory Limit:','')
        if soup.select_one('body > table > tbody > tr > td > div.plm > table > tbody > tr:nth-of-type(2) > td:nth-of-type(5)') is None :
            d['specialjudge'] = 0
        else :
            d['specialjudge'] = 1

        '''
        for key in d :
            print(key,' -->',d[key])
            print('\n'*2)
        '''

        return d


def crawlerFromTo(u,v) :

    pc = PkuCrawler()
    q = Queue()
    for x in range(u,v+1) :
        q.put(x)

    while q.empty() == False :
        pid = q.get()
        time.sleep(0.3)
        try :
            pc.CrawlerProblem(pid)
        except Exception :
            q.put(pid)
            print(pid,' error!!')

def main():
    crawlerFromTo(1000,4050)

if __name__=='__main__' :
    main()