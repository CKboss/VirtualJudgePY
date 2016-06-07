import requests
import random

from Crawler.BzojCrawler.BzojConfig import Bzoj_LogIn_Url, BzojUser,BzojVIPUser


class BzojVjudger:
    submit_url = 'http://www.lydsy.com/JudgeOnline/submit.php'

    def LogIn(self,vip=False):

        self.s = requests.session()
        if vip == False :
            data = random.choice(BzojUser)
        elif vip == True :
            data = random.choice(BzojVIPUser)
        self.s.post(url=Bzoj_LogIn_Url, data=data)
        return data

    def getLanguage(self, lang):

        L = ['C', 'C++', 'Pascal', 'Java']
        ret = 1
        for i in range(0, 4):
            if lang == L[i]:
                return i
        return ret

    def Submit(self, pid, lang, code,vip=True):

        postdata = self.LogIn(vip=vip)

        dt = dict()
        dt['id'] = pid
        dt['language'] = self.getLanguage(lang)
        dt['source'] = code

        self.s.post(self.submit_url, data=dt)

        return postdata['vj_username']


def main():
    bv = BzojVjudger()
    code = '''
    #include
    <dfs
    '''
    bv.Submit('1000', 'C++', code)


if __name__ == '__main__':
    main()
