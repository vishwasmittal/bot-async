import os
from aiohttp import web
from app.main import create_app


def main():
    app = create_app()
    DP_SERVER_HOST = os.getenv('DP_SERVER_HOST', '0.0.0.0')
    DP_SERVER_PORT = os.getenv('DP_SERVER_PORT', '4000')
    web.run_app(app, host=DP_SERVER_HOST, port=int(DP_SERVER_PORT))


if __name__ == '__main__':
    main()
