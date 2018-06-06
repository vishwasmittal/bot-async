from marshmallow import Schema, fields, post_load
from .message import MessageSchema

__all__ = ['UpdateSchema', 'Update']


class Update:
    def __init__(self, update_id, message):
        self.update_id = update_id
        self.message = message


class UpdateSchema(Schema):
    update_id = fields.Int()
    message = fields.Nested(MessageSchema)

    # edited_message = fields.Nested(Message)
    # channel_post = fields.Nested(Message)
    # edited_channel_post = fields.Nested(Message)
    # inline_query = fields.Nested(InlineQuery)
    # chosen_inline_result
    # callback_query
    # shipping

    @post_load
    def get_update_object(self, data):
        return Update(**data)
