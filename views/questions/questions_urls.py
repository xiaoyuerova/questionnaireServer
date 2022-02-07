from __future__ import unicode_literals
from views.questions.questions_views import (
    CreateHandler,
)

urls = [
    (r'create', CreateHandler)
]
