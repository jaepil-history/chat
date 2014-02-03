# Copyright (c) 2013-2014 Appspand, Inc.

from auth import urls as auth_urls
from user import urls as user_urls
from group import urls as group_urls
from message import urls as message_urls


handlers = auth_urls.handlers + user_urls.handlers\
        + group_urls.handlers + message_urls.handlers
