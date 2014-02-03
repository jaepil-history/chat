# Copyright (c) 2013-2014 Appspand, Inc.

import datetime

import message.controller
import models


def create(user_uid, user_name, platform_id=None, device_token=None):
    devices = []
    if platform_id and device_token:
        devices.append(models.DeviceInfo(platform_id=platform_id,
                                         device_token=device_token))

    now = datetime.datetime.utcnow()
    user_info = models.User(uid=user_uid,
                            name=user_name,
                            devices=devices,
                            created_at=now,
                            last_login_at=now)

    return user_info.save()


def find_one(user_uid):
    return models.User.objects(uid=user_uid).first()


def find(user_uids):
    result = models.User.objects(uid__in=user_uids)

    users = []
    for user in result:
        users.append(user)

    return users


def login(user_uid, user_name):
    user_info = find_one(user_uid=user_uid)
    if not user_info:
        user_info = create(user_uid=user_uid, user_name=user_name)

    now = datetime.datetime.utcnow()

    user_info.name = user_name
    user_info.last_login_at = now
    user_info.save()

    return user_info


def logout(user_uid):
    pass


def unregister(user_uid):
    return message.controller.clear_all(user_uid=user_uid, recipient_uid=0, is_group=False)
