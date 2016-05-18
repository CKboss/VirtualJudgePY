import requests
import random


class HduVJudger:
    login_url = 'http://acm.hdu.edu.cn/userloginex.php?action=login'
    submit_url = 'http://acm.hdu.edu.cn/submit.php?action=submit'
    s = None
    nowJudge = None
    snt = 0

    userList = [
        dict(
            username='xxx111',
            nickname='henryascend',
            userpass='heihei',
            login='Sign in',
        ),
        dict(
            username='xxx111',
            nickname='henryascend',
            userpass='heihei',
            login='Sign in',
        ),
    ]

    submit_data = dict(
        check=0,
        problemid=1000,
        language=0,
        usercode='',
    )

    def getlange(self, lang):
        LangeList = ['G++', 'GCC', 'C++', 'C', 'Pascal', 'Java', 'C#']
        for i in range(0, len(LangeList)):
            if LangeList[i] == lang:
                return i
        return 0

    def login(self):
        self.snt = 30
        self.s = requests.session()
        data = random.choice(self.userList)
        self.s.post(url=self.login_url, data=data)
        self.nowJudge = data['nickname']

    def submit(self, pid, lang, code):

        self.login()

        self.submit_data['problemid'] = pid
        self.submit_data['language'] = self.getlange(lang)
        self.submit_data['usercode'] = code

        if self.s == None or self.snt <= 0:
            self.login()
        else:
            self.snt = self.snt - 1

        r = self.s.post(url=self.submit_url, data=self.submit_data)
        #print(r.text)


if __name__ == '__main__':
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

    HV = HduVJudger()
    HV.submit(1000, 'G++', code)
    HV.submit(1000, 'G++', code)
