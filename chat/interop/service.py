# Copyright (c) 2013-2014 Appspand, Inc.

import json
from threading import Thread
from Queue import Queue

from tornado.ioloop import IOLoop

from log import logger
from net.link_manager import LinkManager
import message.controller
import net.protocols

import controller


class QueuePoller(Thread):
    def __init__(self):
        super(QueuePoller, self).__init__()

        self.terminated = False
        self.send_queue = Queue()

    def start(self):
        super(QueuePoller, self).start()

    def stop(self):
        self.terminated = True

    def run(self):
        while not self.terminated:
            logger.access.debug("checking messages from snek queue...")
            items = controller.pull()
            if items:
                IOLoop.instance().add_callback(self.send_to_user, items)

            # while not self.send_queue.empty():
            #     send_req = self.send_queue.get()
            #     controller.push(sender_uid=send_req.sender_uid,
            #                     group_uid=0,
            #                     target_uids=[send_req.target_uid],
            #                     message_info=message_info)
            #     pass

    def send_to_user(self, items):
        for item in items:
            item_data = json.loads(item)
            logger.access.debug("pull from snek: %r" % item_data)

            send_req = net.protocols.Message_SendReq(item_data)
            message.controller.send(sender_uid=send_req.sender_uid,
                                    recipient_uid=send_req.target_uid,
                                    message=send_req.message,
                                    is_group=send_req.is_group)

            # (online, offline) = LinkManager.instance().find(user_uids=send_req.target_uid)
            # if online:
            #     message.controller.send(sender_uid=send_req.sender_uid,
            #                             recipient_uid=send_req.target_uid,
            #                             message=send_req.message,
            #                             is_group=send_req.is_group)
            # else:
            #     self.send_queue.put(send_req)


_started = False
_queue_poller = QueuePoller()


def start():
    global _started
    global _queue_poller

    if _started:
        return

    _queue_poller.start()
    _started = True


def stop():
    global _started
    global _queue_poller

    if _started:
        _started = False
        _queue_poller.stop()
        _queue_poller.join()
