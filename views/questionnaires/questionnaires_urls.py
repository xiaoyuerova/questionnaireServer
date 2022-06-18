from __future__ import unicode_literals
from views.questionnaires.questionnaires_views import (
    CreateHandler,
    GetHandler,
    DeleteHandler,
    SummerGetHandler
)

urls = [
    (r'create', CreateHandler),
    (r'get', GetHandler),
    (r'delete', DeleteHandler),
    (r'summerget', SummerGetHandler)
]
