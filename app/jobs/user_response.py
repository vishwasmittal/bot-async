from marshmallow import Schema, fields, post_load

from app.schema.telegram import *
import json
from app.methods.telegram import sendMessage


# --------------- models & schemas -------------
class Response:
    def __init__(self, text, actions=[]):
        self.text = text
        self.actions = actions


class ResponseSchema(Schema):
    text = fields.Str()
    actions = fields.List(fields.Str)

    @post_load
    def get_object(self, data):
        return Response(**data)


# ------------ methods ------------------------

def get_response(query):
    response_dict = {
        "text": query.text + " -- response",
        "actions": [
            "action 1",
            "action 2",
            "action 3"
        ]
    }

    return ResponseSchema().load(response_dict)


async def send_response(validated_update):
    """
    < JOB >
    Send response to the user for the message in a webhook request
    :param validated_update: telegram.schema.Update object for the webhook request
    :return: Nothing
    """

    # extract the query from the Update object
    # obtain result for this query object
    # serialize this result into the send_message format
    # use telegram methods to send the message

    from app.schema.query_resolver import Query
    print(1)
    query = Query.get_query_from_update(validated_update)

    # get the result for this query
    response = get_response(query)

    # # TODO: remove these things
    # query = Query('message_id', 'date', 'chat', 'message_from', 'response', text=None)
    # response = Response('text', ['actions'])

    query.response = response

    # TODO: format it nicely
    keys = [[KeyboardButton(action) for action in response.actions]]
    reply_keyboard = ReplyKeyboardMarkup(keys)

    final_message = SendMessage(query.chat.id, query.text, reply_markup=reply_keyboard)

    # final json message
    validated_message = SendMessageSchema().dump(final_message)

    print("validated message")
    r = await sendMessage(validated_message)
    print(json.dumps(json.loads(r), indent=4))

# -----------------------------------------------
