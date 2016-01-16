import requests
import re
from bs4 import BeautifulSoup

from dao.problemdao import pdata,InsertProblem

class HduCrawler :

    '''
    HDOJ 编码 gb2312
    '''

    prob_url = 'http://acm.hdu.edu.cn/showproblem.php?pid='

    def CrawlerProblem(self,pid):


        data = pdata.copy()
        data['voj']='HDU'
        data['vid']=pid

        r = requests.get(self.prob_url+str(pid))
        r.encoding = 'gb2312'
        html = r.text
        soup = BeautifulSoup(str(BeautifulSoup(html,'html5lib').select_one('body > table > tbody > tr:nth-of-type(4) > td ')),'html5lib')
        li = soup.select('div[class="panel_content"]')
        title = soup.select_one('html > body > h1')
        data['title']=title.contents[0]

        Terms = ['description','input','output','sampleInput','sampleOutput','source','author'];

        for t in zip([x for x in Terms],[y for y in li]) :
            data[t[0]] = t[1]

        info = str(soup.select('body > font > b > span')[0].contents[0])
        spj = soup.select('body > font > b > span > font')

        if len(spj)!=0 :
            info += "  "
            info += spj[0].contents[0]
        data['problem_limit']=info

        '''
        for x in data :
            print(x +" --> "+str(data[x]))
        '''
        InsertProblem(**data)


if __name__=='__main__' :

    crawler = HduCrawler()
    crawler.CrawlerProblem(5001)
