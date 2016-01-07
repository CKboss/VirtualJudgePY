from __init__ import r,logIn
import requests


class HduSubmit :

    submit_url = 'http://acm.hdu.edu.cn/submit.php?action=submit'

    submit_data = dict(
        check=0,
        problemid=1000,
        language=0,
        usercode='',
    )

    def login(self):
        logIn()

    def getlange(self,lang):
        if lang == 'G++':
            return 0

    def Submit(self,pid,lang,code):

        self.submit_data['language'] = self.getlange(lang)
        self.submit_data['usercode'] = code
        self.submit_data['problemid'] = pid

        r = requests.post(self.submit_url,self.submit_data)

        print(' data : ')
        print(self.submit_data)
        print(' status code : ')
        print(r.status_code)


if __name__=='__main__' :

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

    HS = HduSubmit()
    HS.login()
    print(type(r))
    print(r.cookies)
    #HS.Submit(1000,'G++',code)
