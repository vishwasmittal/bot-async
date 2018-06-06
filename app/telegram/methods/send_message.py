import os

from app.telegram.helpers import make_http_request

__all__ = ['sendMessage']
URL = "https://api.telegram.org/bot{}/sendMessage".format(os.environ.get("BOT_KEY"))


def sendMessage(message):
    make_http_request(URL, data=message, method="POST")
