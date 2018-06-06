import asyncio
from aiohttp import web
from aiojobs.aiohttp import spawn as spawn_job

from app.telegram.schema.types import UpdateSchema
from app.telegram.jobs import message_handler


async def handler(request):
    data = await request.json()
    validated_data = UpdateSchema().load(data)
    # print("This is the handler before spawning the jobs......")
    await spawn_job(request, message_handler(validated_data))
    # print("This is the handler after spawning the jobs")
    return web.Response()
