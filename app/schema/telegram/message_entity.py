from marshmallow import Schema, fields, post_load
from .user import UserSchema

__all__ = ['MessageEntity', 'MessageEntitySchema']


class MessageEntity:
    def __init__(self, type, offset, length, url=None, user=None):
        self.type = type
        self.offset = offset
        self.length = length
        self.url = url
        self.user = user


class MessageEntitySchema(Schema):
    type = fields.Str()
    offset = fields.Int()
    length = fields.Int()
    url = fields.Str(required=False)
    user = fields.Nested(UserSchema, required=False)

    @post_load
    def get_object(self, data):
        return MessageEntity(**data)
