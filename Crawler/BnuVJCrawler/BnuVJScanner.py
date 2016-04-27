import requests
import json
from bs4 import BeautifulSoup
from Crawler.BnuVJCrawler.BnuVJConfig import BnuVJUser

from tools.dbcore import ConnPool
from tools.dbtools import getQueryDetailSQL

class BnuVJScanner:

    s = requests.session()

    scan_url = 'http://www.bnuoj.com/v3/ajax/status_data.php?sEcho=6&iColumns=10&sColumns=&iDisplayStart=0&iDisplayLength=20&mDataProp_0=0&mDataProp_1=1&mDataProp_2=2&mDataProp_3=3&mDataProp_4=4&mDataProp_5=5&mDataProp_6=6&mDataProp_7=7&mDataProp_8=8&mDataProp_9=9&sSearch=&bRegex=false&sSearch_0={username}&bRegex_0=false&bSearchable_0=true&sSearch_1=&bRegex_1=false&bSearchable_1=true&sSearch_2=&bRegex_2=false&bSearchable_2=true&sSearch_3=&bRegex_3=false&bSearchable_3=true&sSearch_4=&bRegex_4=false&bSearchable_4=true&sSearch_5=&bRegex_5=false&bSearchable_5=true&sSearch_6=&bRegex_6=false&bSearchable_6=true&sSearch_7=&bRegex_7=false&bSearchable_7=true&sSearch_8=&bRegex_8=false&bSearchable_8=true&sSearch_9=&bRegex_9=false&bSearchable_9=true&iSortCol_0=1&sSortDir_0=desc&iSortingCols=1&bSortable_0=false&bSortable_1=false&bSortable_2=false&bSortable_3=false&bSortable_4=false&bSortable_5=false&bSortable_6=false&bSortable_7=false&bSortable_8=false&bSortable_9=false&_=1458028215625'

    def languageChange(self,lang):
        if lang == 'GNU C':
            return 'C'
        elif lang == 'GNU C++':
            return 'C++'
        else :
            return 'Java'

    def getOriginOJandProb(self,vpid):

        sql = getQueryDetailSQL('problem','originOJ,originProb',' virtualProb="{}" and virtualOJ="{}"'.format(vpid,'BNUVJ'),' pid ')

        conn = ConnPool.connect()
        cur = conn.cursor()
        cur.execute(sql)
        rt = cur.fetchone()
        cur.close()
        conn.close()

        return rt


    def Analyse(self,html):

        jsondata = json.loads(html)

        n = len(jsondata['aaData'])
        L = list()


        for i in range(0,n) :

            dt = dict()
            dt['virtualOJ'] = 'BNUVJ'

            Title = ['nickname','realrunid','virtualProb','status','language',
                     'runtime','runmemory','codelength','realsubmittime']

            #print(jsondata['aaData'])
            for j in range(0,9):
                dt[Title[j]] = jsondata['aaData'][i][j]

            rt = self.getOriginOJandProb(dt['virtualProb'])

            if rt is not None :
                dt['originOJ'] = rt[0]
                dt['originProb'] = rt[1]

            dt['language'] = self.languageChange(dt['language'])

            L.append(dt)

        return L

    def Scanner(self):

        L = list()

        for x in BnuVJUser:
            url = self.scan_url.format(username=x['username'])
            r = self.s.get(url,timeout=5)

            html = r.text

            #print(html)

            tL = self.Analyse(html)

            L+=tL

        return L


def main():
    bv = BnuVJScanner()
    L = bv.Scanner()
    for li in L :
        print(li)

if __name__=='__main__':
    main()
