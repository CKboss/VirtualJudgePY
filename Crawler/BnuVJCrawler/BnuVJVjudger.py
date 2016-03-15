import requests
import random

from Crawler.BnuVJCrawler.BnuVJConfig import BnuVJ_LogIn_Url,BnuVJUser

class BnuVJVjudge:

    submit_url = 'http://www.bnuoj.com/v3/ajax/problem_submit.php'

    def LogIn(self):
        self.s = requests.session()
        dt = random.choice(BnuVJUser)
        self.s.post(url=BnuVJ_LogIn_Url,data=dt)
        return dt

    def getLanguage(self,lang):
        L = ['','C++','C','Java']
        ret = 1
        for i in range(0,4):
            if lang == L[i]: return i
        return ret

    def Submit(self,pid,lang,code):

        postdata = self.LogIn()

        id = self.getLanguage(lang)

        dt = dict()
        dt['user_id']=postdata['username']
        dt['problem_id']=pid
        dt['language']=self.getLanguage(lang)
        dt['isshare']=1
        dt['source']=code
        dt['login']='Submit'

        self.s.post(url=self.submit_url,data=dt)


def main():
    bv = BnuVJVjudge()
    code = '''#include <iostream>
        using namespace std;
        int main()
        {
        int a,b;
        while(cin>>a>>b)
        {
        cout<<a+b<<endl;
        }
        return 0;
        /* test */ /* test */
        }'''
    bv.Submit('10010','C',code)

if __name__=='__main__':
    main()
