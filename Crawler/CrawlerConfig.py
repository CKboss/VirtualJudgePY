from Crawler.HduCrawler.HduVJudger import HduVJudger
from Crawler.PkuCrawler.PkuVJudger import PkuVJudger
from Crawler.ZojCrawler.ZojVJudger import ZojVJudge
from Crawler.BzojCrawler.BzojVjudger import BzojVjudger

class AutoSubmit():

    def SubmmitSelector(self,oj,prob,lang,code) :

        oj = str(oj).upper()

        if oj == 'HDU' or oj == 'HDOJ':
            HV = HduVJudger()
            HV.submit(prob,lang,code)
        elif oj == 'PKU' or oj == 'POJ' :
            PV = PkuVJudger()
            PV.Sumbit(prob,lang,code)
        elif oj == 'ZOJ' or oj == 'ZJU' :
            ZV = ZojVJudge()
            ZV.Submit(prob,lang,code)
        elif oj == 'BZOJ' or oj == 'LYDSY':
            BV = BzojVjudger()
            BV.Submit(prob,lang,code)
        else :
            print('unkonw oj')