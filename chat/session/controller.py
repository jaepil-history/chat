# Copyright (c) 2013-2014 Appspand, Inc.

import datetime
import hashlib

from config.loader import get_appcfg
from common import cache
from util import timestamp

import models


def create(user_uid):
    appcfg = get_appcfg()
    session_config = appcfg.session

    now = timestamp.get_timestamp()
    issued_at = now
    expires_at = now + datetime.timedelta(
        minutes=session_config.timeout_minutes).total_seconds()
    access_token = hashlib.sha1("%s-%d-%d" % (user_uid, issued_at, expires_at)).hexdigest()

    session = models.Session(user_uid=user_uid,
                             access_token=access_token,
                             issued_at=issued_at,
                             expires_at=expires_at,
                             permissions=[],
                             data={})

    return save(session=session)


def save(session):
    appcfg = get_appcfg()
    redis_config = appcfg.database.redis

    if redis_config.enabled:
        redis = cache.get_connection()
        with redis.pipeline() as tr:
            session_json = session.to_json()

            key = ("session.id:%s" % (session.user_uid))
            tr.set(name=key, value=session_json)
            tr.expireat(key, int(session.expires_at))

            key = ("session.token:%s" % (session.access_token))
            tr.set(name=key, value=session_json)
            tr.expireat(key, int(session.expires_at))

            tr.execute()

        return session
    else:
        return session.save()


def delete(session):
    appcfg = get_appcfg()
    redis_config = appcfg.database.redis

    if redis_config.enabled:
        redis = cache.get_connection()
        with redis.pipeline() as tr:
            tr.delete("session.id:%s" % (session.user_uid))
            tr.delete("session.token:%s" % (session.access_token))

            tr.execute()
    else:
        session.delete()


def find(user_uid=None, access_token=None, extend_token=False, allow_expiration=False):
    appcfg = get_appcfg()
    redis_config = appcfg.database.redis

    session = None
    if redis_config.enabled:
        redis = cache.get_connection()

        session_json = None
        if user_uid:
            session_json = redis.get("session.id:%s" % (user_uid))
        elif access_token:
            session_json = redis.get("session.token:%s" % (access_token))

        if session_json:
            session = models.Session.from_json(session_json)
    else:
        if user_uid:
            session = models.Session.objects(user_uid=user_uid).first()
        elif access_token:
            session = models.Session.objects(access_token=access_token).first()

    if not session:
        # TODO: raise exception
        return None

    if not allow_expiration:
        if is_expired(session=session):
            delete(session=session)
            return None

    if extend_token:
        session = extend(session=session)

    return session


def is_expired(session):
    if not session:
        return False

    now = timestamp.get_timestamp()
    if session.expires_at > now:
        return False

    return True


def renew(session):
    appcfg = get_appcfg()
    session_config = appcfg.session

    if session:
        now = timestamp.get_timestamp()
        expires_at = now + datetime.timedelta(
            minutes=session_config.timeout_minutes).total_seconds()

        session.expires_at = expires_at
        save(session=session)

    return session


def extend(session):
    appcfg = get_appcfg()
    session_config = appcfg.session

    if session:
        now = timestamp.get_timestamp()
        expires_at = now + datetime.timedelta(
            minutes=session_config.timeout_minutes).total_seconds()

        session.expires_at = expires_at
        save(session=session)

    return session


def get_debug_info(access_token):
    return find(access_token=access_token,
                extend_token=False, allow_expiration=True)
