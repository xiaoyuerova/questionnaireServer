from __future__ import unicode_literals
from views.answers.answers_views import (
    SubmitHandler,
    DeleteHandler
)

urls = [
    (r'submit', SubmitHandler),
    (r'delete', DeleteHandler)
]
