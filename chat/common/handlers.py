# Copyright (c) 2013-2014 Appspand, Inc.

import httplib

import tornado.escape
import tornado.gen
import tornado.web

import session.controller
import user.controller


class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application=application, request=request, **kwargs)

    def get_user_info(self, access_token):
        si = session.controller.find(access_token=access_token,
                                     extend_token=True)
        if not si:
            raise tornado.web.HTTPError(httplib.UNAUTHORIZED, reason="Session is expired")

        user_info = user.controller.find_one(user_uid=si.user_uid)
        if not user_info:
            raise tornado.web.HTTPError(httplib.BAD_REQUEST, reason="Invalid user ID")

        return user_info
