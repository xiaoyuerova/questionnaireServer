from __future__ import unicode_literals
from views.questioners.questioners_views import (
    LoginHandler,
    RegisterHandler
)

urls = [
    (r'login', LoginHandler),
    (r'register', RegisterHandler)
]
