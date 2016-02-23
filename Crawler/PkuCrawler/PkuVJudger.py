import requests
import random
import time

from PkuConfig import Pku_User,Pku_LogIn_Url
from tools.encode import UTF8StrToBase64Str,Base64StrToUTF8Str

class PkuVJudger() :

    '''
    1.poj的提交需要对代码进行base64编码
    2.每次都要登陆?
    '''

    headers = { 'User-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2364.103 Safari/537.36',}
    submit_url = 'http://poj.org/submit?action=submit'
    sl = 'http://poj.org/submit?action=submit'
    s = None
    snt = 0

    def LogIn(self):
        self.snt = 30
        self.s = requests.session()
        r = self.s.post(url=Pku_LogIn_Url,data=random.choice(Pku_User))

    def GetLanguage(self,lang):

        L = ['G++','GCC','Java','Pascal','C++','C','Fortran']
        ret = 0
        for i in range(0,7) :
            if lang == L[i] :
                ret = i
                break
        return ret

    def Sumbit(self,pid,lang,code):

        self.LogIn()
        url = self.submit_url
        code = UTF8StrToBase64Str(code)
        d = dict()

        d['problem_id'] = str(pid)
        d['language'] = str(self.GetLanguage(lang))
        d['source'] = code
        d['encoded'] = str(1)

        self.s.post(url=url,data=d)


def main():
    pv = PkuVJudger()
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
    pv.Sumbit(1000,'G++',code)
    pv.Sumbit(1001,'G++',code)

if __name__=='__main__' :
    main()

'''
{'language': '4', 'source': 'CiNpbmNsdWRlIDxpb3N0cmVhbT4KdXNpbmcgbmFtZXNwYWNlIHN0ZDsKaW50IG1haW4oKQp7CiAgICBpbnQgYSxiOwogICAgY2luID4+IGEgPj4gYjsKICAgIGNvdXQgPDwgYStiIDw8IGVuZGw7CiAgICByZXR1cm4gMDsKfQogICAg', 'submit': 'Submit', 'problem_id': '1000', 'encode': '1'}
I2luY2x1ZGUgPGlvc3RyZWFtPiB1c2luZyBuYW1lc3BhY2Ugc3RkOyBpbnQgYSAsYiBjZCM=
'''
