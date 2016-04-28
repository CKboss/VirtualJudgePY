import time
import os
import pickle
import traceback

from Crawler.HduCrawler.HduScanner import HduScanner
from Crawler.PkuCrawler.PkuScanner import PkuScanner
from Crawler.ZojCrawler.ZojScanner import ZojScanner
from Crawler.BzojCrawler.BzojScanner import BzojScanner
from Crawler.BnuVJCrawler.BnuVJScanner import BnuVJScanner

from tools.dbtools import getUpdateSQL
from tools.dbcore import ConnPool

from Config.FilePathConfig import SID_DATA_FILE


class MainScanner():
    TF = SID_DATA_FILE

    def Scanner(self):

        while True:

            try :
                self.Doit()
            except Exception:
                print('Some Exception in Scanner')
                traceback.print_exc()

            time.sleep(5)


    def Doit(self):
        print('-> Before Scanner Stauts: ')
        L = self.FindAndUpdate()
        print('-> End Scanner Stauts: ')

        '''
        print('Len L: ',len(L))
        for li in L : print('----> ',li)
        '''

        files = os.listdir(self.TF)
        for file in files:
            if file.endswith('.pkl'):

                S = pickle.load(open(self.TF + file, 'rb'))
                # print('S:',S)

                for x in L:
                    try :
                        ret = self.CheckIt(S, x)
                    except Exception :
                        print('In check Exception: ')
                        print('S: ',S)
                        print('x: ',x)
                        traceback.print_exc()
                    #print('ret ---> ',ret)
                    if ret is None:
                        continue
                    else:
                        print('here is ret :', ret)
                        # update status
                        clause = 'sid = {}'.format(S['sid'])
                        sql = getUpdateSQL('status', ret, clause)
                        # print('update status sql: ',sql)

                        S['status'] = ret['status']

                        conn = ConnPool.connect()
                        cur = conn.cursor()
                        cur.execute(sql)
                        cur.close()
                        conn.close()

                        break

                        # os.remove(self.TF+file)

                S['looplimit'] = S['looplimit'] - 1
                if S['looplimit'] >= -10:
                    pickle.dump(S, open(self.TF + file, 'wb'))
                else:

                    # Judge Error
                    if 'status' not in S or S['status'] is None or S['status'] == 'Pending':
                        ret = dict()
                        ret['status'] = 'Judge Error'
                        clause = 'sid = {}'.format(S['sid'])
                        sql = getUpdateSQL('status', ret, clause)

                        conn = ConnPool.connect()
                        cur = conn.cursor()
                        cur.execute(sql)
                        cur.close()
                        conn.close()

                    os.remove(self.TF + file)

    def CheckIt(self, s, d):

        # print('s: ',s)
        # print('d: ',d)

        flag = True

        specialOne = False
        try :
            if s['originOJ'] == 'ZOJ' or d['originOJ'] == 'ZOJ':
                specialOne = True
            if s['originOJ'] == 'BZOJ' or d['originOJ'] == 'BZOJ':
                specialOne = True
        except Exception :
            pass

        if d['language'] == 'G++' : d['language'] = 'C++'
        elif d['language'] == 'GCC' : d['language'] = 'C'

        if 'originProb' not in d.keys()  or 'originOJ' not in d.keys() :
            flag = False

        for nt in ['originProb', 'originOJ', 'codelenth', 'language']:

            if specialOne == True and nt == 'codelenth':
                continue

            if flag == False :
                break

            try:
                if s[nt] != d[nt]:
                    # print('item: ',nt,' ',s[nt],' vs ',d[nt])
                    flag = False
                    break
            except Exception:
                print('CheckIt Exception')

        '''
        if s['originOJ'] == 'HDU' and d['originOJ'] == 'HDU' :
            print('s: ',s)
            print('d: ',d)
            print('flag: ',flag)
        '''

        if flag == False:
            return None

        ret = dict()

        for x in ['status', 'runtime', 'runmemory', 'realrunid']:
            ret[x] = d[x]



        return ret

    def FindAndUpdate(self):

        L = list()

        try:
            # print('Start Scanner HDU ...')
            HduS = HduScanner()
            L += HduS.Scanner()
        except Exception:
            print('In HduScanner: ', Exception)

        try:
            # print('Start Scanner PKU ...')
            PkuS = PkuScanner()
            L += PkuS.Scanner()
        except Exception:
            print('In PkuScanner: ', Exception)

        try:
            # print('Start Scanner ZOJ ...')
            Zoj = ZojScanner()
            L += Zoj.Scanner()
        except Exception:
            print('In ZojScanner: ', Exception)

        try:
            Bzoj = BzojScanner()
            L += Bzoj.Scanner()
        except Exception:
            print('In BZojScanner: ', Exception)

        #print(".............. size: ",len(L))
        try:
            Bnuv = BnuVJScanner()
            L += Bnuv.Scanner()
        except Exception:
            print('In BnuVJScanner: ', Exception)

        #print(".............. size: ",len(L))
        return L


def main():
    ms = MainScanner()
    ms.Scanner()

def Test():
    d = {'language': 'C++', 'originOJ': 'HDU', 'nickname': 'henryascend', 'originProb': '1000', 'codelenth': '162', 'runtime': '15MS', 'runmemory': '1796K', 'realrunid': '16997303', 'realsubmittime': '2016-04-26 21:28:11', 'status': 'Accepted'}
    print(d)
    ms = MainScanner()
    s = pickle.load(open('/home/ckboss/Desktop/Development/PKL/sid_120.pkl', 'rb'))
    print(s)

    print(ms.CheckIt(s,d))

if __name__ == '__main__':
    main()
    #Test()
