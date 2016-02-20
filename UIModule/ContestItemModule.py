import tornado.web

class ContestItemModule(tornado.web.UIModule) :

    def render(self, r):
        cid = r[0]
        ctitle = r[1]
        begintime = r[5]
        endtime = r[6]

        status=''
        if r[10] == 0 :
            status = 'Pending'
        elif r[10] == 1 :
            status = 'Running'
        elif r[10] == 2 :
            status = 'Ended'

        return self.render_string('module/contestitem.html',
                           cid=cid,ctitle=ctitle,begintime=begintime,
                           endtime=endtime,status=status)
