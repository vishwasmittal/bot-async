import os

from app.helpers import make_http_request

__all__ = ['sendMessage']
os.environ['BOT_KEY'] = '617361775:AAHS0S6aUQ_gLFmnfOKv72xQj5EBlhBUfos'
URL = "https://api.telegram.org/bot{}/sendMessage".format(os.environ.get("BOT_KEY"))


async def sendMessage(message):
    return await make_http_request(URL, data=message, method="POST")
