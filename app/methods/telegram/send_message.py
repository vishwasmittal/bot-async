import os

from app.helpers import make_http_request

__all__ = ['sendMessage']
URL = "https://api.telegram.org/bot{}/sendMessage".format(os.environ.get("BOT_KEY"))


async def sendMessage(message):
    return await make_http_request(URL, data=message, method="POST")
