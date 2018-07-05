from marshmallow import Schema, fields, post_load
from .message import MessageSchema
from .inline_query import InlineQuerySchema

__all__ = ['UpdateSchema', 'Update']


class Update:
    def __init__(self, update_id, message=None, inline_query=None):
        self.update_id = update_id
        self.message = message
        self.inline_query = inline_query

    def is_inline(self):
        return self.message is None


class UpdateSchema(Schema):
    update_id = fields.Int()
    message = fields.Nested(MessageSchema)
    inline_query = fields.Nested(InlineQuerySchema)

    @post_load
    def get_object(self, data):
        return Update(**data)
