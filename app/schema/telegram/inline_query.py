from datetime import datetime
from marshmallow import Schema, fields, pre_load, post_load
from .user import UserSchema
from .chat import ChatSchema
from .message_entity import MessageEntitySchema

__all__ = ['Message', 'MessageSchema']


class InlineQuery:
    def __init__(self, id, from_user, query, offset):
        self.id = id
        self.from_user = from_user
        self.query = query
        self.offset = offset

    @property
    def chat_id(self):
        return self.from_user.id


class InlineQuerySchema(Schema):
    id = fields.Str()
    from_user = fields.Nested(nested=UserSchema, data_key="from", attribute="from_user", required=False)
    query = fields.Str()
    offset = fields.Str()

    @post_load
    def get_object(self, data):
        return InlineQuery(**data)
