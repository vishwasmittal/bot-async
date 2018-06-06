from marshmallow import Schema, fields, post_load

__all__ = ['UserSchema', 'User']


class User:
    def __init__(self, id, is_bot, first_name, last_name=None, language_code=None, username=None):
        self.id = id
        self.is_bot = is_bot
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.language_code = language_code


class UserSchema(Schema):
    id = fields.Int()
    is_bot = fields.Bool()
    first_name = fields.Str()
    last_name = fields.Str()
    username = fields.Str(required=False)
    language_code = fields.Str()

    @post_load
    def get_object(self, data):
        return User(**data)
