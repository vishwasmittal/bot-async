from marshmallow import Schema, fields, post_load, pre_load

from app.schema.telegram import Message, MessageSchema
from app.jobs.user_response import ResponseSchema

__all__ = ['Query', 'QuerySchema']


class Query(Message):
    def __init__(self, message_id, date, chat, message_from, response=None, **kwargs):
        super().__init__(message_id, date, chat, message_from, **kwargs)
        self.response = response

    @staticmethod
    def get_query_from_update(update):
        # TODO: remove this
        import json
        print("From get_query_from_update\n", json.dumps(MessageSchema().dump(update.message), indent=4))
        message_dump = MessageSchema().dump(update.message)
        return QuerySchema().load(message_dump)


class QuerySchema(MessageSchema):
    response = fields.Nested(ResponseSchema, required=False)

    @pre_load
    def remove_null_fields(self, data):
        if type(data) == dict:
            corr_data = {}
            for key in data:
                temp = self.remove_null_fields(data[key])
                if temp is not None:
                    corr_data[key] = temp
            return corr_data
        else:
            return data

    @post_load
    def get_object(self, data):
        return Query(**data)
