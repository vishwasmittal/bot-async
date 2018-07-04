import asyncio
import aiojobs

from bot_interactor import BotApp
from trade import manager
from managers import interaction
from publish_framework import manager
from publish_framework.news_poller.rss_fetcher_async import main

event_loop = asyncio.get_event_loop()  # async event loop
future = asyncio.ensure_future(aiojobs.create_scheduler())
aiojobs_scheduler = event_loop.run_until_complete(future)  # for execution of async jobs
BotApp.add_async_execs(aiojobs_scheduler)

try:
    main()
    BotApp.start_app()
    event_loop.run_forever()
except Exception as e:
    print(e)
    # BotApp.stop_app()
    # event_loop.stop()
    # event_loop.close()
