import tornado.web

from Config.ParametersConfig import SUPPORT_OJ_LIST

class OJSelectModule(tornado.web.UIModule) :

    def render(self):

        html = '<select size="1" name="oj">'
        html += '<option value="" selected="">All</option>'
        for OJ in SUPPORT_OJ_LIST :
            html += '<option value="{}">{}</option>'.format(OJ,OJ)
        html+='</select>'
        return html
