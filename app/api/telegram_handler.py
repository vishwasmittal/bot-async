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
    print('printing data from handler\n', json.dumps(data))
    update = UpdateSchema().load(data)
    # print(json.dumps(UpdateSchema().dump(update), indent=4))

    if not update.message:
        print("I am here")
        inline_query_id = update.inline_query.id
        results = [
            {
                'type': 'article',
                'id': '1',
                'title': 'title1',
                'input_message_content': {
                    'message_text': 'option 1'
                }
            },
            {
                'type': 'article',
                'id': '2',
                'title': 'title2',
                'input_message_content': {
                    'message_text': 'option 2'
                }
            },
            {
                'type': 'article',
                'id': '3',
                'title': 'title3',
                'input_message_content': {
                    'message_text': 'option 3'
                }
            },
        ]

        from app.schema.telegram.answer_inline_query import InlineQuerySchema
        from app.methods.telegram.repliers import answerInlineQuery

        print(InlineQuerySchema().dumps({'inline_query_id': inline_query_id, 'results': results}))
        inline_query_obj = InlineQuerySchema().load({'inline_query_id': inline_query_id, 'results': results})

        await spawn_job(request, answerInlineQuery(inline_query_id, inline_query_obj.results))


    # TODO: validated data step is transferred to the job below
    # validated_data = UpdateSchema().load(data)
    # json.dump(data, open("webhook_data.json", 'w'))
    # print("spawning jobs")
    # await spawn_job(request, send_response(data))
    # await spawn_job(request, InteractionManager.receive_message(update))
    print("returninig 200 OK")
    return web.Response()
