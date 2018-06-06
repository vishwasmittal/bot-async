from marshmallow import Schema, fields, post_load

from app.schema.telegram import Message, MessageSchema
from app.jobs.user_response import ResponseSchema

__all__ = ['Query', 'QuerySchema']


class Query(Message):
    def __init__(self, message_id, date, chat, message_from, response=None, **kwargs):
        super().__init__(message_id, date, chat, message_from, **kwargs)
        self.response = response

    @staticmethod
    def get_query_from_update(update):
        return QuerySchema().load(MessageSchema().dump(update.message))


class QuerySchema(MessageSchema):
    response = fields.Nested(ResponseSchema, required=False)

    @post_load
    def get_object(self, data):
        return Query(**data)
