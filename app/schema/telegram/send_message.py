from marshmallow import Schema, fields, post_load

from .reply_keyboard_markup import ReplyKeyboardMarkupSchema

__all__ = ['SendMessageBaseSchema', 'ReplyKeyboardMessageSchema',
           "SendMessageSchema", 'SendMessageBase', 'SendMessage', 'ReplyKeyboardMessage']


class SendMessageBase:
    def __init__(self, chat_id, text,
                 parse_mode='Markdown', disable_web_page_preview=None,
                 disable_notification=None, reply_to_message_id=None):
        self.chat_id = chat_id
        self.text = text
        self.parse_mode = parse_mode
        self.disable_web_page_preview = disable_web_page_preview
        self.disable_notification = disable_notification
        self.reply_to_message_id = reply_to_message_id


class ReplyKeyboardMessage(SendMessageBase):
    def __init__(self, chat_id, text, reply_markup, **kwargs):
        super().__init__(chat_id, text, **kwargs)
        self.reply_markup = reply_markup    # ReplyKeyboardMarkup


class SendMessageBaseSchema(Schema):
    chat_id = fields.Int(required=True)
    text = fields.Str(required=True)
    parse_mode = fields.Str(required=False)
    disable_web_page_preview = fields.Bool(required=False)
    disable_notification = fields.Bool(required=False)
    reply_to_message_id = fields.Int(required=False)


class ReplyKeyboardMessageSchema(SendMessageBaseSchema):
    reply_markup = fields.Nested(ReplyKeyboardMarkupSchema, required=False)

    @post_load
    def get_object(self, data):
        return ReplyKeyboardMessage(**data)


SendMessage = ReplyKeyboardMessage
SendMessageSchema = ReplyKeyboardMessageSchema
