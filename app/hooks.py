# Background Tasks

# async def listen_to_redis(app):
#     REDIS_SERVER_HOST = os.getenv('REDSEER_REDIS_HOST', "127.0.0.1")
#     REDIS_SERVER_PORT = os.getenv('REDSEER_REDIS_HOST', "6379")
#     try:
#         sub = await aioredis.create_redis((REDIS_SERVER_HOST, int(REDIS_SERVER_PORT)), loop=app.loop)
#         ch, *_ = await sub.subscribe('news')
#         async for msg in ch.iter(encoding='utf-8'):
#             # Forward message to all connected websockets:
#             for ws in app['websockets']:
#                 ws.send_str('{}: {}'.format(ch.name, msg))
#     except asyncio.CancelledError:
#         pass
#     finally:
#         await sub.unsubscribe(ch.name)
#         await sub.quit()



# async def start_background_tasks(app):
#     app['redis_listener'] = app.loop.create_task(listen_to_redis(app))


async def cleanup_background_tasks(app):
    print("Cleaning Background tasks")
    # await app['apps']['olacabs'].close()
    # app['redis_listener'].cancel()
    # await app['redis_listener']


def setup_hooks(app):
    # app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)
