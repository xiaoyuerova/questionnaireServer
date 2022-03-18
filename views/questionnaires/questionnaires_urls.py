from __future__ import unicode_literals
from views.questionnaires.questionnaires_views import (
    CreateHandler,
    GetHandler,
    DeleteHandler
)

urls = [
    (r'create', CreateHandler),
    (r'get', GetHandler),
    (r'delete', DeleteHandler)
]
