from __future__ import unicode_literals
from views.questioners.questioners_views import (
    LoginHandler,
    ELoginHandler,
    RegisterHandler,
    DeleteHandler
)

urls = [
    (r'login', LoginHandler),
    (r'elogin', ELoginHandler),
    (r'register', RegisterHandler),
    (r'delete', DeleteHandler)
]
