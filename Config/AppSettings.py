import os.path

import tornado.web
import pymysql

from tornado.options import options, define

define('port', default=48888, help='the open port', type=int)

from Handlers.IndexHandler import IndexHandler
from Handlers.LogInHandler import LogInHandler
from Handlers.LogOutHandler import LogOutHandler
from Handlers.RegisterHandler import RegisterHandler
from Handlers.ProblemHandler import ProblemHandler
from Handlers.StatusHandler import StatusHandler
from Handlers.DebugHandler import DebugHandler
from Handlers.ProblemListHandler import ProblemListHandler
from Handlers.RedirectorHandler import RedirectorHandler
from Handlers.SubmitHandler import SubmitHandler
from Handlers.ContestListHandler import ContestListHandler
from Handlers.CreateContestHandler import CreateContestHandler
from Handlers.ManageContestHandler import ManageContestHandler
from Handlers.ManageContestListHandler import ManageContestListHandler
from Handlers.ContestShowHandler import ContestShowHandler
from Handlers.RankListHandler import RankLishHandler
from Handlers.ShowCodeHandler import ShowCodeHandler
from Handlers.UserStatusHandler import UserStatusHander
from Handlers.CrawlerOnlineHandler import CrawlerOnlineHandler
from Handlers.AuthorsRanklistHandler import AuthorsRanklistHandler
from Handlers.ReportBugHandler import ReportBugHandler

from UIModule.HeaderModule import TitleModule
from UIModule.ProblemListModule import ProblemListModule
from UIModule.StatusItemModule import StatusItemModule
from UIModule.ContestItemModule import ContestItemModule
from UIModule.RanklistTableModule import RankListTableModule
from UIModule.OJSelectModule import OJSelectModule
from UIModule.SolvedProblemModule import SolvedProblemModule
from UIModule.ServerTimeModule import ServerTimeModule
from UIModule.ContestProblemListModule import ContestProblemListModule


class AppInit(tornado.web.Application):
    def __init__(self):
        # Url To Handler
        handlers = [
            (r'/', IndexHandler),
            (r'/login\/{0,1}', LogInHandler),
            (r'/logout\/{0,1}', LogOutHandler),
            (r'/register\/{0,1}', RegisterHandler),
            (r'/problem/(\w+)/(\w+)', ProblemHandler),
            (r'/status\/{0,1}', StatusHandler),
            (r'/webdebug', DebugHandler),
            (r'/problemlist', ProblemListHandler),
            (r'/redirection', RedirectorHandler),
            (r'/submit\/{0,1}', SubmitHandler),
            (r'/contestlist\/{0,1}', ContestListHandler),
            (r'/createcontest\/{0,1}', CreateContestHandler),
            (r'/managecontestlist\/{0,1}', ManageContestListHandler),
            (r'/managecontest\/{0,1}', ManageContestHandler),
            (r'/contestshow\/{0,1}', ContestShowHandler),
            (r'/ranklist\/{0,1}', RankLishHandler),
            (r'/showcode\/{0,1}', ShowCodeHandler),
            (r'/userstatus\/{0,1}', UserStatusHander),
            (r'/crawleronline\/{0,1}',CrawlerOnlineHandler),
            (r'/authorsranklist\/{0,1}',AuthorsRanklistHandler),
            (r'/reportbug',ReportBugHandler),
        ]

        # Setting
        settings = dict(

            template_path=os.path.join(os.path.pardir, 'VirtualJudgePY/templates'),
            static_path=os.path.join(os.path.pardir, 'VirtualJudgePY/statics'),
            debug=True,
            gzip=True,
            xsrf_cookies=True,
            cookie_secret='tZJnmMPUSsyQYlXKOWWDVJbuW6Ul9k8IhZ8gF7Aq87E=',
        )

        UI_MODULES = dict(
            HeaderTitle=TitleModule,
            ProblemList=ProblemListModule,
            StatusList=StatusItemModule,
            ContestList=ContestItemModule,
            RankListTable=RankListTableModule,
            OJSelect=OJSelectModule,
            SolvedProblem=SolvedProblemModule,
            ServerTime=ServerTimeModule,
            ContestProblemItem=ContestProblemListModule,
        )

        tornado.web.Application.__init__(self, handlers, ui_modules=UI_MODULES, **settings)


if __name__ == '__main__':
    print(os.path.join(os.path.pardir, 'templates'))
    print(os.path.join(os.path.pardir, 'statics'))
