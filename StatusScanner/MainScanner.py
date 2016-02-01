import time
import os
import pickle

from Crawler.HduCrawler.HduScanner import HduScanner

class MainScanner():

    TF = '/tmp/PKL/'

    def Scanner(self):

        while True:

            time.sleep(3)

            L = self.FindAndUpdate()

            for li in L :
                print('--->' , li)

            files = os.listdir(self.TF)
            for file in files :
                if file.endswith('.pkl') :

                    S = pickle.load(open(self.TF+file,'rb'))
                    print(S)

                    for x in L :
                        ret = self.CheckIt(S,x)
                        #print('---> ',x)
                        if ret is None :
                            continue
                        else :
                            print('here is ret :', ret)


    def CheckIt(self,s,d):
        flag = True

        for nt in ['originProb','originOJ','codelenth','language'] :
            if s[nt] != d[nt] :
                #print('item: ',nt,' ',s[nt],' vs ',d[nt])
                flag=False

        if flag is False:
            return None

        ret = dict()

        for x in ['result','runtime','runmemory','realrunid'] :
            ret[x] = d[x]

        return ret


    def FindAndUpdate(self):

        L = list()

        HduS = HduScanner()
        L += HduS.Scanner()

        return L
        #HDU Scanner


def main():
    ms = MainScanner()
    ms.Scanner()

if __name__=='__main__' :
    main()
