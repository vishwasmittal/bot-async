from marshmallow import Schema, fields, post_load

__all__ = ['Chat', 'ChatSchema']


class Chat:
    def __init__(self, id, type, title=None, username=None, first_name=None, last_name=None):
        self.id = id
        self.type = type
        self.title = title
        self.username = username
        self.first_name = first_name
        self.last_name = last_name


class ChatSchema(Schema):
    id = fields.Int()
    type = fields.Str()
    title = fields.Str(required=False)
    username = fields.Str(required=False)
    first_name = fields.Str(required=False)
    last_name = fields.Str(required=False)

    # all_members_are_administrators
    # photo
    # description
    # invite_link
    # pinned_message
    # sticker_set_name
    # can_set_sticker_set

    @post_load
    def get_object(self, data):
        return Chat(**data)
