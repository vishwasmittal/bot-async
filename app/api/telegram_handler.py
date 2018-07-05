import json

from aiohttp import web
from aiojobs.aiohttp import spawn as spawn_job

from app.schema.telegram.update import UpdateSchema

# from temp_app.app.jobs import send_response

from managers.interaction import InteractionManager

__all__ = ['handler']


# def save_output(data):
#     with open("webhook_data.json", 'w') as file:
#         file.write(data)


async def handler(request):
    data = await request.json()
    # print('printing data from handler\n', json.dumps(data, indent=4))
    update = UpdateSchema().load(data)
    # TODO: validated data step is transferred to the job below
    # validated_data = UpdateSchema().load(data)
    # json.dump(data, open("webhook_data.json", 'w'))
    # print("spawning jobs")
    # await spawn_job(request, send_response(data))
    await spawn_job(request, InteractionManager.receive_message(update))
    # print("returninig 200 OK")
    return web.Response()
