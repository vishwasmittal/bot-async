from app.methods.telegram import sendMessage
from app.schema.query_resolver import Query
from app.schema.telegram import *
from app.schema.telegram.keyboard_button import KeyboardButton

from temp_app.app.methods.response import get_response


def keyboard_layout(actions, row_size=3):
    """
    Returns the layout for the keyboard

    :param actions: list of actions that each key represent
    :param row_size: no. of keys in a single row
    Layout: list of lists specifying the position of each key (with given action) on the keyboard
    """
    layout = []
    for i in range(0, len(actions), row_size):
        layout.append([KeyboardButton(action) for action in actions[i:i + row_size]])
    return layout


def get_keyboard_from_response(response):
    """
    A keyboard is an array of array of rows

    [
        [row 1],\n
        [row 2],
    ]

    :param response: a <class 'schema.response.Response'> instance
    :return: a <class 'schema.telegram.reply_keyboard_markup.ReplyKeyboardMarkup'> instance
    """

    layout = keyboard_layout(response.actions)
    reply_keyboard = ReplyKeyboardMarkup(layout, one_time_keyboard=False)
    return reply_keyboard


async def send_response(validated_update):
    """
    < JOB >
    Send response to the user for the message in a webhook request

    :param validated_update: <class 'telegram.schema.Update'> object for the webhook request

    :return: Nothing
    """

    # TODO: Remove this step from here and set it up in api
    validated_update = UpdateSchema().load(validated_update)

    # get the query object from the webhook message
    # print("validated_update: \n", json.dumps(UpdateSchema().dump(validated_update), indent=4))
    query = Query.get_query_from_update(validated_update)

    # get the result for this query
    response = get_response(query)
    query.response = response  # TODO: add update_id to this query object and save to database

    # obtain a keyboard for the actions to be taken by user
    reply_keyboard = get_keyboard_from_response(response)

    # make the final message object
    final_message = SendMessage(query.chat.id, response.text, reply_markup=reply_keyboard)

    # final json message
    validated_message = SendMessageSchema().dump(final_message)
    # print("validated response\n", json.dumps(validated_message, indent=4))

    # Send the final message to the requesting user
    # print("sending response")
    r = await sendMessage(validated_message)
    # print(json.dumps(json.loads(r), indent=4))
