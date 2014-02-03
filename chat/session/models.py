# Copyright (c) 2013-2014 Appspand, Inc.

from mongoengine import Document
from mongoengine import DictField
from mongoengine import IntField
from mongoengine import ListField
from mongoengine import StringField

from mongoengine import blacklist


class Session(Document):
    user_uid = StringField(required=True, max_length=255)
    access_token = StringField(required=True, max_length=255)
    issued_at = IntField(required=True)
    expires_at = IntField(required=True)
    permissions = ListField(StringField(max_length=255))
    data = DictField()

    meta = {
        "indexes": [
            {"fields": ["user_uid"], "unique": True},
            {"fields": ["access_token"], "unique": True}
        ],
        "roles": {
            "json": {
                "_default": blacklist("id")
            }
        }
    }
