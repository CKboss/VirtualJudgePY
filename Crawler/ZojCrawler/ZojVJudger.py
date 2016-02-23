import requests
import random

from Crawler.ZojCrawler.ZojConfig import Zoj_User,Zoj_LogIn_Url
from tools.encode import UTF8StrToBase64Str,Base64StrToUTF8Str

class ZojVJudge() :

    submit_url = 'http://acm.zju.edu.cn/onlinejudge/submit.do'

    def logIn(self):
        self.snt=30
        self.s = requests.session()
        self.s.post(url=Zoj_LogIn_Url,data=random.choice(Zoj_User))

    def GetLanguage(self,lang):

        L = ['C','C++','FPC','Java','Python','Perl','Scheme','PHP','C++0x']

        ret = 1
        for i in range(0,len(L)) :
            if lang == L[i] :
                ret = i+1
                break
        return ret



    def Submit(self,pid,lang,code):

        self.logIn()

        dt = dict()
        dt['problemId'] = pid-1000
        dt['languageId'] = self.GetLanguage(lang=lang)
        dt['source'] = code

        self.s.post(url=self.submit_url,data=dt)

def main() :
    #ZV = ZojVJudge()
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
    '''
    #ZV.Submit(1001,'C++',code)
    ZV2 = ZojVJudge()
    ZV2.Submit(1002,'C++0x',code+'/*$fdsf*/')

if __name__=='__main__' :
    main()
