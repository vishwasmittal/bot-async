import json

from app.schema.query_resolver import Query
from app.methods.telegram import sendMessage
from app.schema.telegram import *
from app.methods.response import get_response


async def send_response(validated_update):
    """
    < JOB >
    Send response to the user for the message in a webhook request
    :param validated_update: telegram.schema.Update object for the webhook request
    :return: Nothing
    """

    query = Query.get_query_from_update(validated_update)

    # get the result for this query
    response = get_response(query)
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
