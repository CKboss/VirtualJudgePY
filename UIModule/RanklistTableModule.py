import tornado.web


class RankListTableModule(tornado.web.UIModule):
    def render(self, ranklist):

        raw = len(ranklist)
        print('raw: ', raw)
        if raw == 0:
            html = '<table border="1" class="flex-table-item-primary" bordercolor="#FFFFFF" class="text-center"> <tbody> <tr class="tbheader" style="background-color: #1A5CC8; color: #FFFFFF">'
            html += '</tr></tbody></table>'

            return html

        col = len(ranklist[0]['submit'])

        html = '<table border="1" class="flex-table-item-primary text-center" bordercolor="#FFFFFF" class="text-center"> <tbody> <tr class="tbheader" style="background-color: #1A5CC8; color: #FFFFFF">'

        # table head
        html += '<td>Rank</td>'
        html += '<td>User</td>'
        html += '<td>Solved</td>'
        html += '<td>Penalty</td>'
        for i in range(0, col):
            html += '<td>' + str(i + 1000) + '</td>'
        html += '</tr>'

        rank = 1
        for r in ranklist:

            html += '<tr align="center" bgcolor="#f0f8ff">'

            html += '<td>' + str(rank) + '</td>'
            html += '<td><a href="/userstatus?username='+str(r['username'])+'">' + str(r['username']) + '</a></td>'
            html += '<td>' + str(r['totalaccept']) + '</td>'
            html += '<td>' + self.change(int(r['totaltime'])) + '</td>'

            for i in range(0, col):
                html += '<td bgcolor='

                color = '"#f0f8ff"'
                content = ''
                if r['aclist'][i] == 0:
                    if r['submit'][i]==0 :
                        content += ''
                    else :
                        color = '#FFECF5'
                        content += '(-' + str(r['submit'][i]) + ')'
                elif r['aclist'][i] == 1:
                    content += self.change(int(r['ptimelist'][i]))
                    content += '(' + str(r['submit'][i]) + ')'
                    color = "#E0F8EC"
                    if r['firstblood'][i] == 1 :
                        color = "#04B431"

                html += color + '>'
                html += content
                html += '</td>'

            html += '</tr>'

            rank += 1

        html += '</tbody></table>'

        return html

    def change(self,x):
        h,m,s,=x//3600,(x%3600)//60,x%60
        return "%02d:%02d:%02d"%(h,m,s)
