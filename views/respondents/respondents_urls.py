from __future__ import unicode_literals
from views.respondents.respondents_views import (
    RegisterHandler,
    DeleteHandler,
    CompleteHandler
)

urls = [
    (r'register', RegisterHandler),
    (r'delete', DeleteHandler),
    (r'complete', CompleteHandler)
]
