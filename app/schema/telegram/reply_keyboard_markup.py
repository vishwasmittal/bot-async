from marshmallow import Schema, fields, post_load
from .keyboard_button import KeyboardButtonSchema

__all__ = ['ReplyKeyboardMarkup', 'ReplyKeyboardMarkupSchema']


class ReplyKeyboardMarkup:
    def __init__(self, keyboard, one_time_keyboard=False):
        self.keyboard = keyboard
        self.one_time_keyboard = one_time_keyboard


class ReplyKeyboardMarkupSchema(Schema):
    keyboard = fields.List(fields.Nested(KeyboardButtonSchema, many=True))
    one_time_keyboard = fields.Bool()

    @post_load
    def get_object(self, data):
        return ReplyKeyboardMarkup(**data)
