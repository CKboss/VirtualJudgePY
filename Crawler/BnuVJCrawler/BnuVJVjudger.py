import requests
import random

from Crawler.BnuVJCrawler.BnuVJConfig import BnuVJ_LogIn_Url,BnuVJUser

class BnuVJVjudge:

    submit_url = 'https://www.bnuoj.com/v3/ajax/problem_submit.php'

    s = requests.session()

    headers = {
                'Referer':'https://www.bnuoj.com/v3/status.php?showname=JiangOil',
                'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2661.86 Safari/537.36',
                'Origin':'https://www.bnuoj.com',
              }

    def LogIn(self):
        self.s = requests.session()
        self.s.headers = self.headers
        dt = random.choice(BnuVJUser)
        r = self.s.post(url=BnuVJ_LogIn_Url,data=dt,timeout=5)
        #print('in Log in')
        #print(r.text)

        return dt

    def getLanguage(self,lang):
        L = ['','C++','C','Java']
        ret = 1
        for i in range(1,4):
            if lang == L[i]: return i
        return ret

    def Submit(self,pid,lang,code):

        postdata = self.LogIn()
        #print(self.s.cookies)

        dt = dict()
        dt['user_id']=postdata['username']
        dt['problem_id']=pid
        dt['language']=self.getLanguage(lang)
        dt['isshare']=1
        dt['source']=code
        dt['login']='Submit'

        '''
        for key in dt.keys():
            print(key,'--->',dt[key])
        '''
        r = self.s.post(url=self.submit_url,data=dt)
        #print('in submit ',r)
        #print(r.text)
        return postdata['vj_username']

    def debug(self):

        self.s = requests.session()
        self.s.headers = self.headers

        '''
        self.s.get('https://www.bnuoj.com/v3/',verify=True)
        self.s.cookies.set('bnuoj_v3_password','04a49181da1ddb9967dc81122c191e6c36fbaf0a')
        self.s.cookies.set('bnuoj_v3_username','JiangOil')
        '''

        dt = random.choice(BnuVJUser)
        #print(dt)
        r = self.s.post(url=BnuVJ_LogIn_Url,data=dt,timeout=5)

        #print(r)
        #print(r.text)


def main():
    bv = BnuVJVjudge()

    #bv.debug()

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
    bv.Submit('24291','C++',code)

if __name__=='__main__':
    main()
