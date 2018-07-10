import asyncio
from server import main
from publish_framework.news_poller.rss_fetcher_async import main as news_poller_main


from managers.interaction import InteractionManager
from trade.manager import TradeManager
from publish_framework.manager import PublisherManager


news_poller_future = asyncio.ensure_future(news_poller_main())
# loop = asyncio.get_event_loop()
# loop.run_forever()
main()
