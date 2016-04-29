import tornado.web
import time

class ServerTimeModule(tornado.web.UIModule):

    def render(self, *args, **kwargs):
        TIMEFORMATE = '%Y-%m-%d %X'
        return "Server Time(GMT+8): "+time.strftime(TIMEFORMATE,time.localtime())
