import re
import requests
import json

from Crawler.HustCrawler.HustConfig import HustUser

class HustScanner:

    s = requests.session()
    scan_url = 'http://acm.hust.edu.cn/vjudge/problem/fetchStatus.action'

    dt = {
        'draw': '1',
        'columns[0][data]': '0',
        'columns[0][name]': '',
        'columns[0][searchable]': 'true',
        'columns[0][orderable]': 'false',
        'columns[0][search][value]': '',
        'columns[0][search][regex]': 'false',
        'order[0][column]': '0',
        'order[0][dir]': 'desc',
        'start': '0',
        'length': '20',
        'search[value]': '',
        'search[regex]': 'false',
        'un': '',
        'OJId': 'All',
        'probNum': '',
        'res': '0',
        'orderBy': 'run_id',
        'language': '',
    }

    def CheckLanguage(self,lang):

        lang=lang.lower()

        cpp = re.compile(r'.*c\+\+.*')
        gcc = re.compile(r'.*g\+\+.*')
        c = re.compile(r'.*c.*')
        java = re.compile(r'.*java.*')

        m1 = cpp.match(lang)
        m2 = gcc.match(lang)
        m3 = c.match(lang)
        m4 = java.match(lang)

        if m1 is not None or m2 is not None :
            return 'C++'
        elif m3 is not None :
            return 'C'
        elif m4 is not None:
            return 'Java'

    def Analyse(self,d):

        L = list()
        for i in range(0,20):
            try :
                tl = d['data'][i]
            except Exception as e :
                break
            item = dict()
            item['nickname'] = tl[1]
            item['realrunid'] = tl[0]
            item['originOJ'] = tl[11]
            item['originProb'] = tl[12]
            item['runmemory'] = tl[4]
            item['runtime'] = tl[5]
            item['language'] = self.CheckLanguage(tl[6])
            item['status'] = tl[3]
            L.append(item)
            self.CheckLanguage(item['language'])

        return L

    def Scanner(self):

        L = list()

        for x in HustUser :

            postdata = self.dt
            postdata['un'] = x['vj_username']
            r = self.s.post(url=self.scan_url,data=postdata)
            d = json.loads(r.text)
            tL = self.Analyse(d)

            L += tL

        return L


if __name__=='__main__':
    HS = HustScanner()
    L = HS.Scanner()

    for l in L:
        print(l)
