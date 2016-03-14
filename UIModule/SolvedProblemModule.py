import tornado.web


class SolvedProblemModule(tornado.web.UIModule):
    def render(self, r):

        sz = len(r)

        html = '<table><tbody>'

        for i in range(0, sz):
            if i % 10 == 0:
                if i != 0: html += '</tr>'
                html += '<tr>'

            html += '<td><h5><a href="/problem/' + str(r[i][0]) + '/' + str(r[i][1]) + '">' + str(r[i][0]) + str(
                r[i][1]) + '</a></h5></td>'
            html += '<td width="10px"></td>'

            if i == sz - 1:
                html += '</tr>'

        html += '</tbody></table>'

        return html
