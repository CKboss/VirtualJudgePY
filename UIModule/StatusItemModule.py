import tornado.web

class StatusItemModule(tornado.web.UIModule) :

    def render(self, r):

        d = dict()
        d['sid'] = r[0]
        d['username'] = r[11]
        d['oj'] = r[12]
        d['prob'] = r[13]
        d['status'] = r[2]
        if d['status'] == 'Accepted' :
            d['color'] = 'red'
        else :
            d['color'] = 'blue'
        d['runmemory'] = r[4]
        d['runtime'] = r[3]
        d['codelength'] = r[17]
        d['submittime'] = str(r[1])
        d['language'] = r[7]

        return self.render_string('module/StatusItem.html',d=d)
