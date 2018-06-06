from marshmallow import Schema, fields, post_load

__all__ = ['KeyboardButton', 'KeyboardButtonSchema']


class KeyboardButton:
    def __init__(self, text):
        self.text = text


class KeyboardButtonSchema(Schema):
    text = fields.Str()

    @post_load
    def get_keyboard_button(self, data):
        return KeyboardButton(**data)
