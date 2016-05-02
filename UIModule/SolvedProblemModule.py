import tornado.web


class SolvedProblemModule(tornado.web.UIModule):
    def render(self, username, rs):

        print(username,rs)

        sz = len(rs)

        html = '<table><tbody>'

        for i in range(0, sz):
            if i % 10 == 0:
                if i != 0: html += '</tr>'
                html += '<tr>'

            '''
            html += '<td><h5><a href="/problem/' + str(rs[i][0]) + '/' + str(rs[i][1]) + '">' + str(rs[i][0]) + str(
                rs[i][1]) + '</a></h5></td>'
            '''
            html += '<td><h5><a href="/status?problem_id='+str(rs[i][1])+'&user_name='+username+'&oj='+str(rs[i][0])+\
                    '&status=accept&language=&isSearch=isSearch&cid=%">'+ str(rs[i][0])+str(rs[i][1])+'</a></h5></td>'
            html += '<td width="10px"></td>'

            if i == sz - 1:
                html += '</tr>'

        html += '</tbody></table>'

        return html
