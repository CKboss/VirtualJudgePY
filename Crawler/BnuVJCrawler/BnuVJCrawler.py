import requests
import json
from bs4 import BeautifulSoup
from dao.problemdao import InsertOrUpdateProblem
from tools.RandA import RelUrlToAbsUrl


class BnuVJCrawler():

    '''

    ARGUMENTS DETAIL:

    sSearch: problem id
    sSearch_10: search OJ

    '''

    base_url = 'http://www.bnuoj.com/v3/'
    pid_url ='http://www.bnuoj.com/v3/ajax/problem_data.php?sEcho=12&iColumns=12&sColumns=&iDisplayStart=0&iDisplayLength=25&mDataProp_0=0&mDataProp_1=1&mDataProp_2=2&mDataProp_3=3&mDataProp_4=4&mDataProp_5=5&mDataProp_6=6&mDataProp_7=7&mDataProp_8=8&mDataProp_9=9&mDataProp_10=10&mDataProp_11=11&sSearch={}&bRegex=false&sSearch_0=&bRegex_0=false&bSearchable_0=true&sSearch_1=&bRegex_1=false&bSearchable_1=true&sSearch_2=&bRegex_2=false&bSearchable_2=true&sSearch_3=&bRegex_3=false&bSearchable_3=true&sSearch_4=&bRegex_4=false&bSearchable_4=true&sSearch_5=&bRegex_5=false&bSearchable_5=true&sSearch_6=&bRegex_6=false&bSearchable_6=true&sSearch_7=&bRegex_7=false&bSearchable_7=true&sSearch_8=&bRegex_8=false&bSearchable_8=true&sSearch_9=&bRegex_9=false&bSearchable_9=true&sSearch_10={}&bRegex_10=false&bSearchable_10=true&sSearch_11=&bRegex_11=false&bSearchable_11=true&iSortCol_0=1&sSortDir_0=asc&iSortingCols=1&bSortable_0=false&bSortable_1=true&bSortable_2=true&bSortable_3=true&bSortable_4=true&bSortable_5=true&bSortable_6=true&bSortable_7=true&bSortable_8=true&bSortable_9=true&bSortable_10=false&bSortable_11=true&_=1457959454369'
    problem_url='http://www.bnuoj.com/v3/problem_show.php?pid={}'

    realOJname = {'ZOJ':'ZJU',}


    def CrawlerProblem(self,originOJ,originProb):


        OJtype = self.realOJname.get(originOJ,originOJ)
        url1 = self.pid_url.format(originProb,OJtype)
        problem_simp = json.loads(requests.get(url1).text)

        if problem_simp['iTotalDisplayRecords']=='0':
            print('can\'t get problem{}/{}'.format(originOJ,originProb))
            return

        bvid = problem_simp['aaData'][0][1]
        html = requests.get(self.problem_url.format(bvid)).text

        dt = self.GetDetail(html)
        dt['originOJ']=originOJ
        dt['originProb']=originProb
        dt['source']=problem_simp['aaData'][0][3]
        dt['title']=problem_simp['aaData'][0][2]
        dt['virtualOJ']='BNUVJ'
        dt['virtualProb']=problem_simp['aaData'][0][1]
        dt['url']=self.problem_url.format(bvid)

        '''
        for key in dt.keys():
            print(key,' ----> ',dt[key])
            print('.....')
        '''

        Term = ['description', 'input', 'output', 'sampleinput', 'sampleoutput', 'source', 'hint']

        for t in Term:
            if t in dt.keys() :
                dt[t] = RelUrlToAbsUrl(self.base_url, dt[t])

        self.InsertInToDataBase(dt)

    def GetDetail(self,html):

        soup = BeautifulSoup(html,'html5lib')

        dt = dict()

        timelimit = soup.select_one('#conditions > div:nth-of-type(1)').text
        memorylimit = soup.select_one('#conditions > div:nth-of-type(2)').text

        L = soup.find_all(class_='content-wrapper')
        Title = ['description','input','output','sampleinput','sampleoutput','hint']

        for i in range(len(L)):
            try: dt[Title[i]] = L[i]
            except Exception as e:
                print(e)

        dt['specialjudge'] = soup.select_one('#spjinfo')
        if dt['specialjudge'] is None : dt['specialjudge'] = 0
        else: dt['specialjudge'] = 1

        s1 = 'Time Limit: '
        s2 = 'Memory Limit: '
        dt['timelimit'] = timelimit[timelimit.find(s1)+len(s1):]
        dt['memorylimit'] = memorylimit[memorylimit.find(s2)+len(s2):]

        return dt

    def InsertInToDataBase(self,dt):
        InsertOrUpdateProblem(dt)


def main():
    BVC = BnuVJCrawler()
    BVC.CrawlerProblem('HRBUST','1003')
    '''
    f = open('/tmp/h1.html','r')
    html = f.read()
    BVC.GetDetail(html)
    '''

if __name__=='__main__':
    main()
