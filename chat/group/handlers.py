# Copyright (c) 2013-2014 Appspand, Inc.

import re

import tornado.escape
import tornado.gen
import tornado.web

from common.handlers import BaseHandler
import message.controller
import controller


class CreateGroupHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        access_token = self.get_argument("access_token")
        invitee_uids = self.get_argument("invitee_uids")
        title = self.get_argument("title", None)

        user_info = self.get_user_info(access_token=access_token)
        if not user_info:
            pass

        parsed_invitee_uids = []
        if invitee_uids:
            parsed_invitee_uids = re.split(r"\s*[,]\s*", invitee_uids.strip())

        group_info = controller.create(owner_uid=user_info.uid,
                                       invitee_uids=parsed_invitee_uids,
                                       title=title)

        self.write("{")
        self.write("\"group\": ")
        self.write(group_info.to_json())
        self.write("}")

        self.finish()


class DeleteGroupHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        access_token = self.get_argument("access_token")
        group_uid = long(self.get_argument("group_uid"))

        user_info = self.get_user_info(access_token=access_token)
        if not user_info:
            pass

        group_info = controller.delete(group_uid=group_uid, owner_uid=user_info.uid)

        self.write("{")
        self.write("\"group\": ")
        self.write(group_info.to_json())
        self.write("}")

        self.finish()


class ListGroupHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        access_token = self.get_argument("access_token")

        user_info = self.get_user_info(access_token=access_token)
        if not user_info:
            pass

        group_infos = []

        self.write("{\"groups\": [")
        self.write(", ".join(g.to_json() for g in group_infos))
        self.write("]}")

        self.finish()


class InviteUserHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        access_token = self.get_argument("access_token")
        group_uid = long(self.get_argument("group_uid"))
        invitee_uids = self.get_argument("invitee_uids")

        user_info = self.get_user_info(access_token=access_token)
        if not user_info:
            pass

        parsed_invitee_uids = []
        if invitee_uids:
            parsed_invitee_uids = re.split(r"\s*[,]\s*", invitee_uids.strip())

        group_info = controller.invite(group_uid=group_uid, user_uid=user_info.uid,
                                       invitee_uids=parsed_invitee_uids)

        self.write("{")
        self.write("\"group\": ")
        self.write(group_info.to_json())
        self.write("}")

        self.finish()


class JoinGroupHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        access_token = self.get_argument("access_token")
        group_uid = long(self.get_argument("group_uid"))

        user_info = self.get_user_info(access_token=access_token)
        if not user_info:
            pass

        group_info = controller.join(group_uid=group_uid, user_uid=user_info.uid)

        self.write("{")
        self.write("\"group\": ")
        self.write(group_info.to_json())
        self.write("}")

        self.finish()


class LeaveGroupHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        access_token = self.get_argument("access_token")
        group_uid = long(self.get_argument("group_uid"))

        user_info = self.get_user_info(access_token=access_token)
        if not user_info:
            pass

        message.controller.clear_all(user_uid=user_info.uid,
                                     recipient_uid=group_uid,
                                     is_group=True)
        group_info = controller.leave(group_uid=group_uid, user_uid=user_info.uid)

        self.write("{")
        self.write("\"group\": ")
        self.write(group_info.to_json())
        self.write("}")

        self.finish()
