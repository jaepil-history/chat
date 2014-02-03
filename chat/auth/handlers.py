# Copyright (c) 2013-2014 Appspand, Inc.

import httplib

import tornado.gen
import tornado.web

from common.handlers import BaseHandler
import session.controller


class RequestAccessTokenHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        email = self.get_argument("user_uid")

        si = session.controller.find(user_uid=email, extend_token=True)
        if not si:
            si = session.controller.create(user_uid=email)
            if not si:
                raise tornado.web.HTTPError(httplib.UNAUTHORIZED, reason="Unauthorized user")

        self.write("{")
        self.write("\"session\": ")
        self.write(si.to_json())
        self.write("}")

        self.finish()

    @tornado.web.asynchronous
    def post(self):
        email = self.get_argument("user_uid")

        si = session.controller.find(user_uid=email, extend_token=True)
        if not si:
            si = session.controller.create(user_uid=email)
            if not si:
                raise tornado.web.HTTPError(httplib.UNAUTHORIZED, reason="Unauthorized user")

        self.write("{")
        self.write("\"session\": ")
        self.write(si.to_json())
        self.write("}")

        self.finish()


class DebugAccessTokenHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        access_token = self.get_argument("access_token")

        si = session.controller.find(access_token=access_token, extend_token=False)
        if si:
            self.write("{")
            self.write("\"session\": ")
            self.write(si.to_json())
            self.write("}")
        else:
            self.set_status(404, "Invalid access token")

        self.finish()


class VerifyAccessTokenHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        access_token = self.get_argument("access_token")

        si = session.controller.find(access_token=access_token, extend_token=False)
        if si:
            self.write("{")
            self.write("\"session\": ")
            self.write(si.to_json())
            self.write("}")
        else:
            self.set_status(404, "Invalid access token")

        self.finish()
