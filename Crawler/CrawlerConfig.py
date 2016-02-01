from Crawler.HduCrawler.HduCrawler import HduCrawler
from Crawler.HduCrawler.HduVJudger import HduVJudger

class AutoSubmit():

    def __init__(self):
        self.HV = HduVJudger()

    def SubmmitSelector(self,oj,prob,lang,code) :

        if oj == 'HDU' or oj == 'HDOJ':
            self.HV.submit(prob,lang,code)
        else :
            print('unkonw oj')