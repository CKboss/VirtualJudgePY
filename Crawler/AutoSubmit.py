from Crawler.HduCrawler.HduVJudger import HduVJudger
from Crawler.PkuCrawler.PkuVJudger import PkuVJudger
from Crawler.ZojCrawler.ZojVJudger import ZojVJudge
from Crawler.BzojCrawler.BzojVjudger import BzojVjudger
from Crawler.BnuVJCrawler.BnuVJVjudger import BnuVJVjudge
from Crawler.HustCrawler.HustVJudger import HustVJudger

from tools.dbcore import ConnPool
from tools.dbtools import FetchOne
from tools.dbtools import getQueryDetailSQL

class AutoSubmit():
    def SubmmitSelector(self, oj, prob, lang, code):

        roj = oj
        oj = str(oj).upper()
        vj_username = None

        if oj == 'HDU' or oj == 'HDOJ':
            HV = HduVJudger()
            vj_username = HV.submit(prob, lang, code)
        elif oj == 'PKU' or oj == 'POJ':
            PV = PkuVJudger()
            vj_username = PV.Sumbit(prob, lang, code)
        elif oj == 'ZOJ' or oj == 'ZJU':
            ZV = ZojVJudge()
            vj_username = ZV.Submit(prob, lang, code)
        elif oj == 'BZOJ' or oj == 'LYDSY':
            BV = BzojVjudger()
            vj_username = BV.Submit(prob, lang, code)
        else:

            rs = self.getPID(roj,prob)
            if rs is None : return None
            if rs[0] is None: return None
            pid = rs[1]
            if rs[0] == 'HUST':
                HUST = HustVJudger()
                vj_username = HUST.Submit(roj,pid,lang,code)
            elif rs[0] == 'BNUVJ' :
                BVJ = BnuVJVjudge()
                vj_username = BVJ.Submit(pid,lang,code)

        return vj_username

    def getPID(self,oj,prob):
        sql = getQueryDetailSQL('problem',' virtualOJ,virtualProb ',' originOJ = "{}" and originProb = "{}" '.format(oj,prob),' pid ')
        rs = FetchOne(sql)
        return rs

if __name__=='__main__':
    AS = AutoSubmit()
    #ans = AS.getPID('HDU',1002)
    #ans = AS.getPID('Aziu',"0001")
    code='abcdefghijklmnopqristubwasfa'*3
    AS.SubmmitSelector('Aizu',"0000",'C++',code)
