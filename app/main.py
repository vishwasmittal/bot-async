import base64
from pathlib import Path

import aiohttp_jinja2
from aiojobs.aiohttp import setup as setup_aiojobs

import jinja2
from aiohttp import web

import aiohttp_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from .settings import Settings
from .views import index, message_data, messages

THIS_DIR = Path(__file__).parent
BASE_DIR = THIS_DIR.parent

from .routes import setup_routes
from .hooks import setup_hooks
from .cors import setup_cors
from .middleware import setup_middlewares
from .database import setup_database


def create_app():
    app = web.Application()
    settings = Settings()
    app.update(
        name='todel',
        settings=settings
    )

    # jinja2_loader = jinja2.FileSystemLoader(str(THIS_DIR / 'templates'))
    # aiohttp_jinja2.setup(app, loader=jinja2_loader)

    secret_key = base64.urlsafe_b64decode(settings.COOKIE_SECRET)
    aiohttp_session.setup(app, EncryptedCookieStorage(secret_key))

    setup_middlewares(app)
    setup_database(app)

    setup_routes(app)
    setup_hooks(app)
    # Enable cors after adding routes
    # setup_cors(app)
    setup_aiojobs(app)
    return app

# def setup_routes(app):
#     app.router.add_get('/', index, name='index')
#     app.router.add_route('*', '/messages', messages, name='messages')
#     app.router.add_get('/messages/data', message_data, name='message-data')


# def create_app():
#     app = web.Application()
#     settings = Settings()
#     app.update(
#         name='todel',
#         settings=settings
#     )

#     # jinja2_loader = jinja2.FileSystemLoader(str(THIS_DIR / 'templates'))
#     # aiohttp_jinja2.setup(app, loader=jinja2_loader)

#     secret_key = base64.urlsafe_b64decode(settings.COOKIE_SECRET)
#     aiohttp_session.setup(app, EncryptedCookieStorage(secret_key))

#     setup_routes(app)
#     return app
