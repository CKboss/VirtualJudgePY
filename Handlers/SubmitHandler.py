from Handlers.BaseHandler import BaseHandler
from Crawler.CrawlerConfig import AutoSubmit

class SubmitHandler(BaseHandler):

    def prepare(self):
        self.AS = AutoSubmit()

    def get(self, *args, **kwargs):

        OJ = self.get_argument('OJ',None)
        Prob = self.get_argument('Prob',None)
        self.get_current_user()

        if OJ is None or Prob is None :
            return

        ret = str(self.current_user)+OJ+Prob

        if len(self.current_user) == 0 :
            self.write('<h1>Please LogIn first!!!</h1>')
        else :
            self.render('submit.html',OJ=OJ,Prob=Prob)


    def post(self, *args, **kwargs):

        Prob = self.get_argument('Prob',None)
        lang = self.get_argument('language',None)
        code = self.get_argument('usercode',None)
        oj = self.get_argument('OJ',None)

        if lang is None or len(code)==0 or oj is None or code is None :
            self.write('<h1>Submit Error!!</h1>')
        else :
            print('lang: ',lang,' oj: ',oj,' Prob: ',Prob,' code ',code,'user: ',self.current_user)
            self.AS.SubmmitSelector(oj=oj,pid=Prob,lang=lang,code=code)
            self.write('<h1>Submit Success!!</h1>')


    def SubmmitCollector(self):
        pass
