#!/usr/bin/env python
#
# Copyright (c) 2013-2014 Appspand, Inc.

import json
import sys

from tornado import httpclient


SERVER_BASE_URL = "http://localhost:8400/v1"


def do_auth(argv):
    user_uid = argv[0]

    request_url = "%s/auth/access_token?user_uid=%s" % (SERVER_BASE_URL, user_uid)
    client = httpclient.HTTPClient()
    response = client.fetch(request=request_url,
                            connect_timeout=10.0,
                            request_timeout=10.0)
    print response.body
    client.close()


def do_login(argv):
    access_token = argv[0]
    name = argv[1]

    request_url = "%s/user/login?access_token=%s&name=%s" % (SERVER_BASE_URL, access_token, name)
    client = httpclient.HTTPClient()
    response = client.fetch(request=request_url,
                            connect_timeout=10.0,
                            request_timeout=10.0)
    print response.body
    client.close()


def do_message_send(argv):
    access_token = argv[0]
    recipient_uid = argv[1]
    group_uid = argv[2]
    message = argv[3]
    secret = argv[4]

    request_url = "%s/message/send?access_token=%s\
                &recipient_uid=%s&group_uid=%s&message=%s&secret=%s"
                % (SERVER_BASE_URL, access_token, recipient_uid, group_uid, message, secret)
    client = httpclient.HTTPClient()
    response = client.fetch(request=request_url,
                            connect_timeout=10.0,
                            request_timeout=10.0)
    print response.body
    client.close()


def do_message_get(argv):
    access_token = argv[0]
    sender_uid = argv[1]
    group_uid = argv[2]
    since_uid = argv[3]
    count = argv[4]

    request_url = "%s/message/get?access_token=%s\
                &sender_uid=%s&group_uid=%s&since_uid=%s&count=%s"
                % (SERVER_BASE_URL, access_token, sender_uid, group_uid, since_uid, count)
    client = httpclient.HTTPClient()
    response = client.fetch(request=request_url,
                            connect_timeout=10.0,
                            request_timeout=10.0)
    print response.body
    client.close()


def do_message_read(argv):
    access_token = argv[0]
    message_uids = argv[1]

    request_url = "%s/message/read?access_token=%s&message_uids=%s"
                % (SERVER_BASE_URL, access_token, message_uids)
    client = httpclient.HTTPClient()
    response = client.fetch(request=request_url,
                            connect_timeout=10.0,
                            request_timeout=10.0)
    print response.body
    client.close()


def do_message_open(argv):
    access_token = argv[0]
    message_uid = argv[1]

    request_url = "%s/message/open?access_token=%s&message_uid=%s"
                % (SERVER_BASE_URL, access_token, message_uid)
    client = httpclient.HTTPClient()
    response = client.fetch(request=request_url,
                            connect_timeout=10.0,
                            request_timeout=10.0)
    print response.body
    client.close()


def do_message_cancel(argv):
    access_token = argv[0]
    message_uid = argv[1]

    request_url = "%s/message/cancel?access_token=%s&message_uid=%s"
                % (SERVER_BASE_URL, access_token, message_uid)
    client = httpclient.HTTPClient()
    response = client.fetch(request=request_url,
                            connect_timeout=10.0,
                            request_timeout=10.0)
    print response.body
    client.close()


def do_group_create(argv):
    access_token = argv[0]
    message_uid = argv[1]

    request_url = "%s/group/create?access_token=%s&message_uid=%s"
                % (SERVER_BASE_URL, access_token, message_uid)
    client = httpclient.HTTPClient()
    response = client.fetch(request=request_url,
                            connect_timeout=10.0,
                            request_timeout=10.0)
    print response.body
    client.close()


def do_group_delete(argv):
    pass


def do_group_invite(argv):
    pass


def do_group_join(argv):
    pass


def do_group_leave(argv):
    pass


def main():
    if len(sys.argv) < 2:
        print "client.py [action]"
        return 1

    action = sys.argv[1]

    if action == "auth":
        do_auth(sys.argv[2:])
    elif action == "login":
        do_login(sys.argv[2:])
    elif action == "message.get":
        do_message_get(sys.argv[2:])
    elif action == "message.send":
        do_message_send(sys.argv[2:])
    elif action == "message.read":
        do_message_read(sys.argv[2:])
    elif action == "message.open":
        do_message_open(sys.argv[2:])
    elif action == "message.cancel":
        do_message_cancel(sys.argv[2:])
    elif action == "group.create":
        do_group_create(sys.argv[2:])
    elif action == "group.delete":
        do_group_delete(sys.argv[2:])
    elif action == "group.invite":
        do_group_invite(sys.argv[2:])
    elif action == "group.join":
        do_group_join(sys.argv[2:])
    elif action == "group.leave":
        do_group_leave(sys.argv[2:])

    return 0


if __name__ == "__main__":
    main()
