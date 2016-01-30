import tornado.web

class RedirectorHandler(tornado.web.RequestHandler):

    def get(self):
        pass

    def post(self, *args, **kwargs):

        msg = self.get_argument('msg',None)

        if msg is None :
            print('msg is None')
            return

        returl = '/'
        if msg[:3] == 'pl_' :
            self.ProblemListSolution(msg)
            returl = self.ProblemListSolution(msg)

        self.redirect(returl)


    def ProblemListSolution(self,msg):

        index = self.get_cookie('pl_index','0')
        index = int(index)

        if msg == 'pl_prev' :
            index = index - 20
        elif msg == 'pl_next' :
            index = index + 20
        elif msg == 'pl_top' :
            index = 0

        if index < 0 : index = 0
        index = str(index)

        pl_oj = self.get_cookie('pl_oj','')
        pl_problem_id = self.get_cookie('pl_problem_id','')
        pl_problem_title = self.get_cookie('pl_problem_title','')
        pl_problem_source = self.get_cookie('pl_problem_source','')

        self.set_cookie('pl_index',index)

        redr_url = '/problemlist?oj={}&problem_id={}&problem_title={}&problem_source={}&index={}'\
            .format(pl_oj,pl_problem_id,pl_problem_title,pl_problem_source,index)

        return redr_url

