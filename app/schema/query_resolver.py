from marshmallow import post_load

from app.schema.telegram import Message, MessageSchema

__all__ = ['Query', 'QuerySchema']


class Query(Message):
    @staticmethod
    def get_query_from_update(update):
        return QuerySchema().load(MessageSchema().dump(update.message))


class QuerySchema(MessageSchema):
    @post_load
    def get_object(self, data):
        return Query(**data)
