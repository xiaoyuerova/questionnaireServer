from __future__ import unicode_literals
from views.questions.questions_views import (
    CreateHandler,
    DeleteHandler
)

urls = [
    (r'create', CreateHandler),
    (r'delete', DeleteHandler)
]
