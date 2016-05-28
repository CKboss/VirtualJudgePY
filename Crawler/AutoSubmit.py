from Crawler.HduCrawler.HduVJudger import HduVJudger
from Crawler.PkuCrawler.PkuVJudger import PkuVJudger
from Crawler.ZojCrawler.ZojVJudger import ZojVJudge
from Crawler.BzojCrawler.BzojVjudger import BzojVjudger
from Crawler.BnuVJCrawler.BnuVJVjudger import BnuVJVjudge

from tools.dbcore import ConnPool
from tools.dbtools import getQueryDetailSQL

class AutoSubmit():
    def SubmmitSelector(self, oj, prob, lang, code):

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
            BVJ = BnuVJVjudge()
            rs = self.getPID(oj,prob)
            if rs is None :
                print(' no such prob ...')
            else :
                pid = rs[0]
                vj_username = BVJ.Submit(pid,lang,code)
        return vj_username

    def getPID(self,oj,prob):

        sql = getQueryDetailSQL('problem',' virtualProb ',' originOJ = "{}" and originProb = "{}" and virtualOJ = "BNUVJ" '.format(oj,prob),' pid ')

        conn = ConnPool.connect()
        cur = conn.cursor()
        cur.execute(sql)
        rs = cur.fetchone()

        return rs
