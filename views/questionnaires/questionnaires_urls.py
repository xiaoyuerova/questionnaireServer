from __future__ import unicode_literals
from views.questionnaires.questionnaires_views import (
    CreateHandler,
    GetHandler
)

urls = [
    (r'create', CreateHandler),
    (r'get', GetHandler)
]
