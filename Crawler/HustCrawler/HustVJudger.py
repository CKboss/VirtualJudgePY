import requests
import random

from tools.encode import UTF8StrToBase64Str,Base64StrToUTF8Str

from Crawler.HustCrawler.HustConfig import HustUser

class HustVJudger:

    login_url = 'http://acm.hust.edu.cn/vjudge/user/login.action'
    submit_url = 'http://acm.hust.edu.cn/vjudge/problem/submit.action'


    def LogIn(self):
        postdata = random.choice(HustUser)
        self.s = requests.session()
        r = self.s.post(url=self.login_url,data=postdata)
        return postdata

    def getLanguate(self,oj,lang):

        lange = dict()
        lange['HDU']={'C++':0,'C':3,'Java':5}
        lange['PKU']={'C++':0,'C':1,'Java':2}
        lange['ACdream']={'C':1,'C++':2,'Java':3}
        lange['Aizu']={'C':'C','C++':'C++','Java':'JAVA'}
        lange['CodeForces']={'Java':36,'C++':1,'C':10}
        lange['SGU']={'C++':'GNU CPP (MinGW, GCC 4)','C':'GNU C (MinGW, GCC 4)','Java':'JAVA 7'}
        lange['ZOJ']={'C':1,'C++':2,'Java':4}
        lange['BZOJ']={'C':0,'C++':1,'Java':3}

        dt = lange[oj]
        for x in dt.keys():
            if x==lang : return dt[x]

        return 0

    def Submit(self,oj,pid,lang,code):

        postdata = self.LogIn()

        dt=dict()

        dt['language']=self.getLanguate(oj=oj,lang=lang)
        dt['isOpen']=1
        dt['source']=UTF8StrToBase64Str(code)
        dt['id']=pid

        r = self.s.post(url=self.submit_url,data=dt)

        return postdata['vj_username']


if __name__=='__main__':

    HV = HustVJudger()
    code = '''
    #include <iostream>

    using namespace std;

    int main()
    {
    int a,b;
    while(cin>>a>>b)
    {
    cout<<a+b<<endl;
    }
    return 0;
    }
    sdfasdfasdfa
    asdfafa
    asfasdfasfasf
    asdfasdfasfaf
    '''
    HV.Submit('CodeForces',50144,'C++',code)
