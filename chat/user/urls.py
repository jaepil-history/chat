# Copyright (c) 2013-2014 Appspand, Inc.

import handlers


handlers = [
    (r"/v1/user/login", handlers.LoginHandler),
    (r"/v1/user/unregister", handlers.UnregisterHandler),
]
