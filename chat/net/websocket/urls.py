# Copyright (c) 2013-2014 Appspand, Inc.

import net.websocket.handlers


handlers = [
    (r"/v1/ws", net.websocket.handlers.WebSocketHandler)
]
