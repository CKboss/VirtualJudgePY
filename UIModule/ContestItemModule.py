import tornado.web


class ContestItemModule(tornado.web.UIModule):
    def render(self, r):
        cid = r[0]
        ctitle = r[1]
        begintime = r[5]
        endtime = r[6]

        status = ''
        color = ''
        if r[10] == 0:
            status = 'Pending'
            color = 'green'
        elif r[10] == 1:
            status = 'Running'
            color = 'red'
        elif r[10] == 2:
            status = 'Ended'
            color = 'grey'

        return self.render_string('module/contestitem.html',
                                  cid=cid, ctitle=ctitle, begintime=begintime,
                                  endtime=endtime, status=status, color=color)
