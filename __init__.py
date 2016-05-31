import tornado.httpserver
import tornado.ioloop

from Config.AppSettings import options, AppInit
from StatusScanner.MainScanner import MainScanner
from ContestScanner.ContestScanner import ContestScanner

import threading

class WebThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        self.tornado_web()

    def tornado_web(self):
        tornado.options.parse_command_line()
        app = AppInit()
        http_server = tornado.httpserver.HTTPServer(app)
        http_server.listen(options.port)
        tornado.ioloop.IOLoop.instance().start()


class ScannerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        self.MainScanner()

    def MainScanner(self):
        ms = MainScanner()
        ms.Scanner()


class ContestScannerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        self.ContestScanner()

    def ContestScanner(self):
        cs = ContestScanner()
        cs.mainloop()

if __name__ == "__main__":
    thread_web = WebThread()
    thread_scanner = ScannerThread()
    thread_contestscanner = ContestScannerThread()

    thread_web.start()
    thread_contestscanner.start()
    thread_scanner.start()
