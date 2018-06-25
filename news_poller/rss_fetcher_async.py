import asyncio

import feedparser
from aiohttp import ClientSession

from new_app.news_poller.models import RSSSchema

list_sources = [
    'https://timesofindia.indiatimes.com/rssfeedstopstories.cms?x=1',
    'http://indianexpress.com/feed',
    'http://www.thehindu.com/news/national/?service=rss',
    'http://www.news18.com/rss/india.xml',
    'http://www.firstpost.com/feed/rss',
]


async def fetch(url, session):
    async with session.get(url) as response:
        return await response.read()


async def get_feed(source, session):
    response = await fetch(source, session)
    print("fetched from {}".format(source))
    # parse the feeds here
    parsed = feedparser.parse(response)
    feed = RSSSchema().load(parsed)  # feed will be and RSS object. Check models.py for reference
    print("categories for the data: {}".format(feed.items[0].category))
    # TODO: send the serialized objects as soon as they are fetched
    return feed


async def run():
    tasks = []
    async with ClientSession() as session:
        for url in list_sources:
            print("fetching from {}".format(url))
            # await get_feed(source=url, session=session)
            task = asyncio.ensure_future(get_feed(url, session))
            tasks.append(task)
        return await asyncio.gather(*tasks)


def print_responses(result):
    print(result)


async def runner(callback):
    while True:
        feeds = await run()
        # TODO: process the RSS objects like logging them
        callback(feeds[0].items[0].link)
        await asyncio.sleep(10)

# if __name__ == "__main__":
#
#     loop = asyncio.get_event_loop()
#     future = asyncio.ensure_future(runner())
#     try:
#         # loop.run_forever()
#         loop.run_until_complete(future)
#     finally:
#         loop.close()
