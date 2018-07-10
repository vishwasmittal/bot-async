from aiohttp import web
from aiojobs.aiohttp import spawn as spawn_job

from app.schema.telegram.update import UpdateSchema
from app.methods.telegram.repliers import answerInlineQuery

from managers.interaction import InteractionManager

__all__ = ['handler']


async def handler(request):
    data = await request.json()
    update = UpdateSchema().load(data)
    if update.is_inline():
        inline_query_id = update.inline_query.id
        await spawn_job(request, answerInlineQuery(inline_query_id))
    else:
        await spawn_job(request, InteractionManager.receive_message(update))
    return web.Response()
