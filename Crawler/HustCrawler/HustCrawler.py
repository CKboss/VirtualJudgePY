import requests
import re
import json

from bs4 import BeautifulSoup

from tools.RandA import RelUrlToBase64Code
from dao.problemdao import InsertOrUpdateProblem

class HustCrawler():

    prob_url = 'http://acm.hust.edu.cn/vjudge/problem/listProblem.action'
    getprog_url = 'http://acm.hust.edu.cn/vjudge/dwr/fetchDescriptions.action'
    virtual_url = 'http://acm.hust.edu.cn/vjudge/problem/viewProblem.action?id={}'

    prob_post = {
        'draw': '5',
        'columns[0][data]': '0',
        'columns[0][name]': '',
        'columns[0][searchable]': 'false',
        'columns[0][orderable]': 'false',
        'columns[0][search][value]': '',
        'columns[0][search][regex]': 'false',
        'order[0][column]': '3',
        'order[0][dir]': 'desc',
        'start': '0',
        'length': '20',
        'search[value]': '',
        'search[regex]': 'false',
        'OJId': 'HDU',
        'probNum': '3006',
        'title': '',
        'source': '',
    }

    def CrawlerProblem(self,oj,pid):

        postdata = self.prob_post
        noj = oj
        '''
        if noj in OJ_Nicname.keys() :
            noj = OJ_Nicname[noj]
        '''
        postdata['OJId'] = noj
        postdata['probNum'] = pid

        data = dict()
        data['originOJ']=oj
        data['originProb']=pid

        r = requests.get(url=self.prob_url,params=postdata)
        dt = json.loads(str(r.text))
        data['title']=dt['data'][0][2]
        realid = dt['data'][0][5]
        r = requests.get(url=self.getprog_url,params=dict(pid=realid))
        dt = json.loads(str(r.text))[0]

        referer = 'http://acm.hust.edu.cn/vjudge/problem/viewProblem.action?id='+str(realid)

        RTAlist = ['description','output','input','sampleInput','sampleOutput']

        for key in dt.keys():
            if key in RTAlist:
                dt[key]=RelUrlToBase64Code(baseurl='',text=dt[key],referer=referer,checkpicture=False)

        data['url']=self.virtual_url.format(realid)
        data['virtualOJ']='HUST'
        data['virtualProb']=realid

        Terms = ['description', 'input', 'output', 'sampleInput', 'sampleOutput', 'source', 'author','hint'];

        for item in Terms :
            if item in dt.keys() :
                data[item.lower()] = dt[item]
            else :
                data[item.lower()] = ''

        html = requests.get(data['url']).text
        soup = BeautifulSoup(html,'html5lib')
        limit = str(soup.select_one('#left_view > div.plm > table').text).replace(' ','').replace('\t','').replace('\n',' ')
        try :
            data['timelimit'],data['memorylimit']=self.getLimit(line=limit)
        except Exception as e:
            pass

        data['specialjudge']=0
        InsertOrUpdateProblem(data)

        '''
        for key in data :
            print(key,'--->',data[key])
        '''

    def getLimit(self,line):
        pattern = r'.*TimeLimit:(.*)MemoryLimit:(.*)64bitIOFormat:(.*)'
        m = re.match(pattern,line)
        return m.group(1).replace(' ',''),m.group(2).replace(' ','')

def testre():
    line = '   TimeLimit:  2000MS    MemoryLimit:  65536KB    64bitIOFormat: %lld&%llu '
    pattern = r'.*TimeLimit:(.*)MemoryLimit:(.*)64bitIOFormat:(.*)'
    m = re.match(pattern,line)

    print(m)
    print(m.group(1))
    print(m.group(2))

if __name__=='__main__':
    HC = HustCrawler()
    HC.CrawlerProblem('Aizu','0000')
