from marshmallow import Schema, fields, post_load
from .keyboard_button import KeyboardButtonSchema

__all__ = ['ReplyKeyboardMarkup', 'ReplyKeyboardMarkupSchema']


class ReplyKeyboardMarkup:
    def __init__(self, keyboard):
        self.keyboard = keyboard


class ReplyKeyboardMarkupSchema(Schema):
    keyboard = fields.Nested(KeyboardButtonSchema, many=True)

    @post_load
    def get_reply_keyboard_markup(self, data):
        return ReplyKeyboardMarkup(**data)
