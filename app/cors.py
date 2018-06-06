import aiohttp_cors


def setup_cors(app):
    # `aiohttp_cors.setup` returns `aiohttp_cors.CorsConfig` instance.
    # The `cors` instance will store CORS configuration for the
    # application.
    cors = aiohttp_cors.setup(app, defaults={
        # Allow all to read all CORS-enabled resources from
        # *.
        "*": aiohttp_cors.ResourceOptions(),
    })

    # Configure CORS on all routes.
    for route in list(app.router.routes()):
        cors.add(route)
