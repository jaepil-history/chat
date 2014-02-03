# Copyright (c) 2013-2014 Appspand, Inc.

import re

import tornado.escape
import tornado.gen
import tornado.web

from common.handlers import BaseHandler
import controller


class GetSummaryHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        access_token = self.get_argument("access_token")
        # count = self.get_argument("count", None)

        user_info = self.get_user_info(access_token=access_token)
        if not user_info:
            pass

        # TODO: recent 1 message for each group, unread message count
        controller.get_summary(user_uid=user_info.uid)

        self.finish()


class GetMessagesHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        access_token = self.get_argument("access_token")
        target_uid = self.get_argument("target_uid", None)
        since_uid = self.get_argument("since_uid", None)
        count = self.get_argument("count", None)
        message_uids = self.get_argument("message_uids", None)
        group = self.get_argument("group", False)

        user_info = self.get_user_info(access_token=access_token)
        if not user_info:
            pass

        parsed_message_uids = None
        if message_uids:
            parsed_message_uids = re.split(r"\s*[,]\s*", message_uids.strip())
        message_infos = controller.get(src_uid=user_info.uid, dest_uid=target_uid,
                                       since_uid=since_uid, count=count,
                                       message_uids=parsed_message_uids,
                                       is_group=group)

        self.write("{\"messages\": [")
        self.write(", ".join(m.to_json() for m in message_infos))
        self.write("]}")

        self.finish()


class SendMessageHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        access_token = self.get_argument("access_token")
        recipient_uid = self.get_argument("recipient_uid", None)
        group_uid = self.get_argument("group_uid", None)
        message = self.get_argument("message")
        secret = (int(self.get_argument("secret", 0)) != 0)

        user_info = self.get_user_info(access_token=access_token)
        if not user_info:
            pass

        message_info = controller.send(sender_uid=user_info.uid,
                                       recipient_uid=recipient_uid,
                                       group_uid=group_uid,
                                       message=message, is_secret=secret)

        self.write("{")
        self.write("\"message\": ")
        self.write(message_info.to_json())
        self.write("}")

        self.finish()


class ReadMessageHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        access_token = self.get_argument("access_token")
        message_uids = self.get_argument("message_uids")

        user_info = self.get_user_info(access_token=access_token)
        if not user_info:
            pass

        parsed_message_uids = re.split(r"\s*[,]\s*", message_uids.strip())
        message_infos = controller.read(user_uid=user_info.uid,
                                        message_uids=parsed_message_uids)

        self.write("{\"messages\": [")
        self.write(", ".join(m.to_json() for m in message_infos))
        self.write("]}")

        self.finish()


class OpenMessageHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        access_token = self.get_argument("access_token")
        message_uid = long(self.get_argument("message_uid"))

        user_info = self.get_user_info(access_token=access_token)
        if not user_info:
            pass

        message_info = controller.open_secret_message(user_uid=user_info.uid,
                                                      message_uid=message_uid)

        self.write("{")
        self.write("\"message\": ")
        self.write(message_info.to_json())
        self.write("}")

        self.finish()


class CancelMessageHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        access_token = self.get_argument("access_token")
        recipient_uid = self.get_argument("recipient_uid", None)
        group_uid = self.get_argument("group_uid", None)
        message_uid = long(self.get_argument("message_uid"))

        user_info = self.get_user_info(access_token=access_token)
        if not user_info:
            pass

        message_info = controller.cancel(sender_uid=user_info.uid,
                                         recipient_uid=recipient_uid,
                                         group_uid=group_uid,
                                         message_uid=message_uid)

        self.write("{")
        self.write("\"message\": ")
        self.write(message_info.to_json())
        self.write("}")

        self.finish()


class ClearMessageHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        access_token = self.get_argument("access_token")
        recipient_uid = self.get_argument("recipient_uid", None)
        group_uid = self.get_argument("group_uid", None)

        user_info = self.get_user_info(access_token=access_token)
        if not user_info:
            pass

        try:
            controller.clear_all(user_uid=user_info.uid,
                                 recipient_uid=recipient_uid, group_uid=group_uid)
        except:
            pass

        self.finish()
