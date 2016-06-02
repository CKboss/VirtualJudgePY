import tornado.web

from Config.ParametersConfig import SUPPORT_OJ_LIST


class OJSelectModule(tornado.web.UIModule):
    def render(self,firstoj='ALL'):
        if firstoj==' ': firstoj='ALL'
        html = '<select size="1" name="oj">'
        html += '<option value="'+firstoj+'" selected="">'+firstoj+'</option>'
        for OJ in SUPPORT_OJ_LIST:
            if OJ == firstoj : OJ = 'ALL'
            html += '<option value="{}">{}</option>'.format(OJ, OJ)
        html += '</select>'
        return html
