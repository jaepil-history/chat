# Copyright (c) 2013-2014 Appspand, Inc.

# import hashlib
import datetime

from common import cache
from util import idgen

from config.loader import get_appcfg
import event.controller

import models


def _save(group_info):
    config = get_appcfg()

    if config.database.redis.enabled:
        redis = cache.get_connection()
        key = ("group.%s" % group_info.uid)
        json = group_info.to_json()
        redis.set(name=key, value=json)
    else:
        group_info.save()

    return group_info


def _load(group_uid):
    config = get_appcfg()

    group_info = None
    if config.database.redis.enabled:
        redis = cache.get_connection()
        key = ("group.%s" % group_uid)
        json = redis.get(name=key)
        if not json:
            # TODO: raise exception
            pass
        group_info = models.Group.from_json(json)
    else:
        group_info = models.Group.objects(uid=group_uid).first()

    return group_info


def create(owner_uid, invitee_uids, title=None):
    uid = idgen.get_next_id()
    members = [owner_uid] + invitee_uids
    now = datetime.datetime.utcnow()
    group_info = models.Group(uid=uid,
                              title=title,
                              owner=owner_uid,
                              members=members,
                              created_at=now)

    _save(group_info=group_info)

    return group_info


def delete(owner_uid, group_uid):
    pass


def find(group_uid):
    return _load(group_uid=group_uid)


def invite(group_uid, user_uid, invitee_uids):
    if not group_uid:
        # TODO: raise exception
        return None

    group_info = find(group_uid=group_uid)
    if not group_info:
        return None

    for uid in invitee_uids:
        if uid not in group_info.members:
            group_info.members.append(uid)

    _save(group_info=group_info)

    event.controller.on_user_invited(group_uid=group_uid,
                                     user_uid=user_uid,
                                     invitee_uids=invitee_uids)

    return group_info


def join(group_uid, user_uid):
    if not group_uid:
        # TODO: raise exception
        return None

    group_info = find(group_uid=group_uid)
    if not group_info:
        return None

    if user_uid not in group_info.members:
        group_info.members.append(user_uid)

    _save(group_info=group_info)

    event.controller.on_user_joined(user_uid=user_uid,
                                    group_uid=group_uid)

    return group_info


def leave(group_uid, user_uid):
    group_info = find(group_uid=group_uid)
    if not group_info:
        # TODO: raise exception
        return None

    if user_uid not in group_info.members:
        return None

    group_info.members.remove(user_uid)

    _save(group_info=group_info)

    event.controller.on_user_leaved(user_uid=user_uid,
                                    group_uid=group_uid,
                                    target_uids=group_info.members)

    return group_info
