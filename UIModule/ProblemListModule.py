import tornado.web


class ProblemListModule(tornado.web.UIModule):
    def render(self, t):
        problemID = t[5]
        OJ = t[4]
        title = t[1]
        source = t[2]
        url = '/problem/' + OJ + '/' + problemID
        return self.render_string('module/problemList.html', oj=OJ, id=problemID, title=title, source=source, url=url)
