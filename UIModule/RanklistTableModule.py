import tornado.web

class RankListTableModule(tornado.web.UIModule) :

    def render(self,ranklist):


        raw = len(ranklist)
        print('raw: ',raw)
        if raw == 0 :

            html = '<table border="1" class="flex-table-item-primary" bordercolor="#FFFFFF" class="text-center"> <tbody> <tr class="tbheader" style="background-color: #1A5CC8; color: #FFFFFF">'
            html += '</tr></tbody></table>'

            return html

        col = len(ranklist[0]['submit'])

        html = '<table border="1" class="flex-table-item-primary" bordercolor="#FFFFFF" class="text-center"> <tbody> <tr class="tbheader" style="background-color: #1A5CC8; color: #FFFFFF">'

        #table head
        html += '<td>Rank</td>'
        html += '<td>AC</td>'
        html += '<td>User</td>'
        for i in range(0,col) :
            html += '<td>'+str(i+1000)+'</td>'
        html += '</tr>'

        rank = 1
        for r in ranklist :

            html += '<tr>'

            html += '<td>'+str(rank)+'</td>'
            html += '<td>'+str(r['totalaccept'])+'</td>'
            html += '<td>'+str(r['username'])+'</td>'

            for i in range(0,col) :
                html += '<td>'

                content = ''
                if r['aclist'][i] == 0 :
                    content += '('+str(r['submit'][i])+')'
                elif r['aclist'][i] == 1 :
                    content += str(r['ptimelist'][i])

                html += content
                html += '</td>'

            html += '</tr>'

        html += '</tbody></table>'

        return html
