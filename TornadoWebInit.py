import tornado.httpserver
import tornado.ioloop

from Config.AppSettings import options, AppInit

def tornado_web():
    tornado.options.parse_command_line()
    app = AppInit()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__=='__main__':
    tornado_web()
