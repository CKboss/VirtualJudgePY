import tornado.web

class ContestProblemListModule(tornado.web.UIModule) :

    def render(self,tr,cid,nt,r,a,totalsubmit,acsubmit):

        tn = totalsubmit.get(r[2],0)
        an = acsubmit.get(r[2],0)

        d = 0.0
        if tn!=0 : d = an*100/tn

        if a == 1 : color = '#E0F8EC'
        radio = '{}%({}/{})'.format(d,an,tn)

        color = '#f0f8ff'
        ac = ''
        if a == 1 :
            ac = 'Y'
            color = '#E0F8EC'
        elif tr==1 :
            ac = 'N'
            color = '#FFECF5'

        return self.render_string('module/ContestProblemList.html',ac=ac,cid=cid,nt=nt,color=color,radio=radio,r=r)
