from marshmallow import Schema, fields

from .reply_keyboard_markup import ReplyKeyboardMarkupSchema

__all__ = ['SendMessageBaseSchema', 'ReplyKeyboardMessageSchema', "SendMessageSchema"]


class SendMessageBaseSchema(Schema):
    chat_id = fields.Int(required=True)
    text = fields.Str(required=True)
    parse_mode = fields.Str(required=False)
    disable_web_page_preview = fields.Bool(required=False)
    disable_notification = fields.Bool(required=False)
    reply_to_message_id = fields.Int(required=False)


class ReplyKeyboardMessageSchema(SendMessageBaseSchema):
    reply_markup = fields.Nested(ReplyKeyboardMarkupSchema, required=False)


SendMessageSchema = ReplyKeyboardMessageSchema
