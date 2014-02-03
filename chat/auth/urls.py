# Copyright (c) 2013-2014 Appspand, Inc.

import handlers


handlers = [
    (r"/v1/auth/access_token", handlers.RequestAccessTokenHandler),
    (r"/v1/auth/debug_token", handlers.DebugAccessTokenHandler),
    (r"/v1/auth/verify_token", handlers.VerifyAccessTokenHandler),
    # (r"/v1/session/(?P<access_token>\w+)/(?P<action>\w+)", handlers.SessionHandler)
]
