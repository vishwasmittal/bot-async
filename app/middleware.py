# def error_pages(overrides):
#     @web.middleware
#     async def middleware(request, handler):
#         try:
#             response = await handler(request)
#             override = overrides.get(response.status)
#             if override is None:
#                 return response
#             else:
#                 return await override(request, response)
#         except web.HTTPException as ex:
#             override = overrides.get(ex.status)
#             if override is None:
#                 raise
#             else:
#                 return await override(request, ex)
#     return middleware


# TODO: Change this to rest api
# async def handle_404(request, response):
#     response = aiohttp_jinja2.render_template('404.html',
#                                               request,
#                                               {})
#     return response

# # TODO: Change this to rest api
# async def handle_500(request, response):
#     response = aiohttp_jinja2.render_template('500.html',
#                                               request,
#                                               {})
#     return response

def setup_middlewares(app):
    # error_middleware = error_pages({404: handle_404,
    #                                 500: handle_500})
    # app.middlewares.append(error_middleware)
    pass