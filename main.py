import tornado.web
import tornado.ioloop

import os

from tornado.options import define, options
from common.url_router import include, url_wrapper
from common.models import init_db

from conf.base import (
    SERVER_PORT,
    SERVER_HEADER
)
from views.questioners.questioners_views import LoginHandler


class Application(tornado.web.Application):
    def __init__(self):
        init_db()
        handles = url_wrapper([
            (r"/", LoginHandler),
            (r"/questioners/", include('views.questioners.questioners_urls')),
            (r"/questionnaires/", include('views.questionnaires.questionnaires_urls')),
            (r"/questions/", include('views.questions.questions_urls')),
            (r"/respondents/", include('views.respondents.respondents_urls')),
            (r"/answers/", include('views.answers.answers_urls')),
            (r"/summer/", include('views.summer.summer_urls')),
        ])
        settings = dict(
            debug=True,
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            csrf_cookies=False
        )
        tornado.web.Application.__init__(self, handles, **settings)


if __name__ == '__main__':
    print("Tornado server is ready for service\r")
    print("run in " + SERVER_HEADER)
    tornado.options.parse_command_line()
    Application().listen(SERVER_PORT, xheaders=True)
    tornado.ioloop.IOLoop.instance().start()
