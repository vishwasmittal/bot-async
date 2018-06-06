from aiohttp import web
from aiojobs.aiohttp import spawn as spawn_job

from app.jobs import send_response
from app.schema import UpdateSchema

__all__ = ['handler']


# def save_output(data):
#     with open("webhook_data.json", 'w') as file:
#         file.write(data)


async def handler(request):
    data = await request.json()
    validated_data = UpdateSchema().load(data)
    print("request received")
    # json.dump(data, open("webhook_data.json", 'w'))
    await spawn_job(request, send_response(validated_data))
    return web.Response()
