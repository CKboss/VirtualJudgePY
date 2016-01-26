import requests
import time
import pickle
from bs4 import BeautifulSoup

class HduCrawler :

    '''
    HDOJ 编码 gb2312
    '''

    prob_url = 'http://acm.hdu.edu.cn/showproblem.php?pid='

    def CrawlerProblem(self,pid):


        data = dict()
        data['originOJ']='HDU'
        data['originProb']=pid
        data['url'] = self.prob_url+str(pid)

        r = requests.get(data['url'])
        r.encoding = 'gb2312'
        html = r.text
        soup = BeautifulSoup(str(BeautifulSoup(html,'html5lib').select_one('body > table > tbody > tr:nth-of-type(4) > td ')),'html5lib')
        li = soup.select('div[class="panel_content"]')
        title = soup.select_one('html > body > h1')
        data['title']=title.contents[0]

        Terms = ['description','input','output','sampleinput','sampleoutput','source','author'];

        for t in zip([x for x in Terms],[y for y in li]) :
            data[t[0]] = t[1]

        data['source'] = BeautifulSoup(str(data['source']),'html5lib').text

        info = str(soup.select('body > font > b > span')[0].contents[0])
        spj = soup.select('body > font > b > span > font')

        if len(spj)!=0 :
            info += "  "
            info += spj[0].contents[0]

        L = checkLimitInfo(info)

        data['specialjudge'] = L[0]
        data['timelimit'] = L[1]
        data['memorylimit'] = L[2]

        data['updatetime'] = time.strftime('%Y-%m-%d %H:%M:%S')

        f = open('/home/ckboss/Desktop/Development/testData/HDOJ/HDOJ{}.pkl'.format(pid),'wb')
        pickle.dump(data,f)

        print(str(pid)+' done !')
        '''
        for x in data :
            print(x +" --> "+str(data[x]))
        '''
        #InsertProblem(**data)


def checkLimitInfo(s) :
    '''
    from limit info to get timelimit memorylimit spj
    :param s:
    :return: L[spj,timelimit,memorylimit]
    '''

    L = list()

    p1 = s.find('Time Limit: ')
    p2 = s.find('Memory Limit: ')
    p3 = s.find('Special Judge')

    if p3==-1 :
        p3 = len(s)+1
        L.append(False)
    else :
        L.append(True)

    L.append(s[p1+12:p2-1])
    L.append(s[p2+14:p3])

    return L

def test1() :
    s = ' Time Limit: 30000/15000 MS (Java/Others)    Memory Limit: 65536/65536 K (Java/Others)  Special Judge'

    L = checkLimitInfo(s)
    print(L)

    s = 'Time Limit: 2000/1000 MS (Java/Others)    Memory Limit: 65536/65536 K (Java/Others)'

    print('-'*30)

    L = checkLimitInfo(s)
    print(L[1])

def test2() :
    f = open('/tmp/HDOJ5001.pkl','rb')
    dt = pickle.load(f)
    soup = BeautifulSoup(str(dt['source']),'html5lib')
    print(soup.text)

def test3() :

    crawler = HduCrawler()
    for x in range(5290,5600) :
        try :
            crawler.CrawlerProblem(x)
            time.sleep(5)
        except Exception :
            print('%d error!!!'%x)

if __name__=='__main__' :
    test3()
    '''
    crawler = HduCrawler()
    crawler.CrawlerProblem(5001)
    crawler.CrawlerProblem(5011)
    crawler.CrawlerProblem(4756)
    '''
