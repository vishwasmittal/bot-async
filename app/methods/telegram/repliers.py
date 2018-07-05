import os

from app.helpers import make_http_request
from app.schema.telegram.send_message import SendMessage, SendMessageSchema
from app.schema.telegram.answer_inline_query import InlineQuery, InlineQuerySchema

__all__ = ['sendMessage']
os.environ['BOT_KEY'] = '617361775:AAHS0S6aUQ_gLFmnfOKv72xQj5EBlhBUfos'
URL = "https://api.telegram.org/bot{}/sendMessage".format(os.environ.get("BOT_KEY"))
template_url = "https://api.telegram.org/bot{}/{}".format(os.environ.get("BOT_KEY"), {})


def get_validated_message(to, text, reply_markup):
    reply_message_object = SendMessage(to, text, reply_markup=reply_markup)
    validated_message = SendMessageSchema().dump(reply_message_object)
    return validated_message


def get_validated_inline_answer(inline_query_id, results):
    inline_query_answer = InlineQuery(inline_query_id, results)
    validated_answer = InlineQuerySchema().dump(inline_query_answer)
    return validated_answer


async def sendMessage(to, text, reply_markup):
    message = get_validated_message(to, text, reply_markup)
    url = template_url.format('sendMessage')
    return await make_http_request(url, data=message, method="POST")


async def answerInlineQuery(inline_query_id, results):
    answer = get_validated_inline_answer(inline_query_id, results)
    url = template_url.format('answerInlineQuery')
    return print(await make_http_request(url, data=answer, method="POST"))
