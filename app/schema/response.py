from marshmallow import Schema, fields, post_load


class Response:
    def __init__(self, text, actions=None):
        if actions is None:
            actions = []
        self.text = text
        self.actions = actions


class ResponseSchema(Schema):
    text = fields.Str()
    actions = fields.List(fields.Str)

    @post_load
    def get_object(self, data):
        return Response(**data)
