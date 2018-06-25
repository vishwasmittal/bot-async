import asyncio

from news_poller.rss_fetcher_async import runner
from new_app.bot import BotApp
from new_app.publishers.news_publisher import NewsPublisher
from new_app.action import Action, StartAction

NewsPublisher.publisher_callback = BotApp.send_message
loop = asyncio.get_event_loop()
future = asyncio.ensure_future(runner(NewsPublisher.publish))

# trade = Action('trade', 'C')
# subscriptions = Action('subscriptions', 'C')
# leave = Action('leave', 'C')
#
# StartAction.add_actions([trade, subscriptions, leave])




try:
    # loop.run_forever()
    BotApp.start_app()
    loop.run_until_complete(future)
except Exception as e:
    print(e)
    BotApp.stop_app()
finally:
    loop.close()
