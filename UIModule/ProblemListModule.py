import tornado.web


class ProblemListModule(tornado.web.UIModule):
    def render(self, t,ac,tr):
        problemID = t[5]
        OJ = t[4]
        title = t[1]
        source = t[2]
        url = '/problem/' + OJ + '/' + problemID
        color = '#f0f8ff'
        if ac == 1 : color = '#E0F8EC'
        elif tr==1 : color='#FFECF5'
        return self.render_string('module/problemList.html',color = color, oj=OJ, id=problemID, title=title, source=source, url=url)
