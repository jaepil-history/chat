# Copyright (c) 2013-2014 Appspand, Inc.

import handlers


handlers = [
    (r"/v1/message/get", handlers.GetMessagesHandler),
    (r"/v1/message/summary", handlers.GetSummaryHandler),
    (r"/v1/message/send", handlers.SendMessageHandler),
    (r"/v1/message/read", handlers.ReadMessageHandler),
    (r"/v1/message/open", handlers.OpenMessageHandler),
    (r"/v1/message/cancel", handlers.CancelMessageHandler),
    (r"/v1/message/clear", handlers.ClearMessageHandler),
]
