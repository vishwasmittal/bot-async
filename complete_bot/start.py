from complete_bot.library_bot_sample import *
from complete_bot.action_handlers import *
from complete_bot.publishers.news_publisher import NewsPublisher
from complete_bot.news_poller.rss_fetcher_async import runner
import asyncio

start = Action(trigger='start', kind='C', handler=on_start)
unsubscribe = Action(trigger='unsubscribe', kind='C', handler=on_unsubscribe)
abort = Action(trigger='abort', kind='C', handler=on_abort)
unknown = Action(trigger=Filters.command, kind='M', handler=on_unknown)
message = Action(trigger=Filters.text, kind='M', handler=on_message)
# news = Action(trigger='news', kind='C', handler=on_news)
trade = Action(trigger='trade', kind='C', handler=on_trade)

# news_source = Action(trigger="news_source", kind='M', handler=get_news)

start.add_actions([trade, unsubscribe])
# news.add_actions([abort, unsubscribe])
trade.add_actions([abort, unsubscribe])

# import json
# print(json.dumps(start.export_action(), indent=4))

bot_app = BotApp(start_action=start)
bot_app.start_app()

publisher = NewsPublisher()
publisher.publisher_callback = bot_app.send_message
loop = asyncio.get_event_loop()
future = asyncio.ensure_future(runner(publisher.publish))
try:
    # loop.run_forever()
    loop.run_until_complete(future)
finally:
    loop.close()
