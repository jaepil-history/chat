# Copyright (c) 2013-2014 Appspand, Inc.

import handlers


handlers = [
    (r"/v1/group/create", handlers.CreateGroupHandler),
    (r"/v1/group/delete", handlers.DeleteGroupHandler),
    (r"/v1/group/list", handlers.ListGroupHandler),
    (r"/v1/group/invite", handlers.InviteUserHandler),
    (r"/v1/group/join", handlers.JoinGroupHandler),
    (r"/v1/group/leave", handlers.LeaveGroupHandler),
]
