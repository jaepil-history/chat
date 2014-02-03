# Copyright (c) 2013-2014 Appspand, Inc.

import queue.models


def create(user_uid):
    q = queue.models.Queue(user_uid=user_uid)
    q.save()

    return q


def find_one(user_uid):
    return queue.models.Queue.objects(user_uid=user_uid).first()


def find(user_uids):
    result = queue.models.Queue.objects(user_uid__in=user_uids)

    queues = []
    for q in result:
        queues.append(q)

    return queues
