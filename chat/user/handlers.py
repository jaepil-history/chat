# Copyright (c) 2013-2014 Appspand, Inc.

import httplib

import tornado.escape
import tornado.gen
import tornado.web

from common.handlers import BaseHandler
import session.controller
import controller


class LoginHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        access_token = self.get_argument("access_token")
        user_name = self.get_argument("name")

        si = session.controller.find(access_token=access_token,
                                     extend_token=True)
        if not si:
            raise tornado.web.HTTPError(httplib.UNAUTHORIZED, reason="Session is expired")

        user_info = controller.login(user_uid=si.user_uid, user_name=user_name)
        self.write("{")
        self.write("\"me\": ")
        self.write(user_info.to_json())
        self.write("}")

        self.finish()


class UnregisterHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        self.finish()
