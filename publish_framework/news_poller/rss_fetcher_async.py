import asyncio
from aiohttp import ClientSession
import feedparser

from publish_framework.news_poller.models import RSSSchema

list_sources = [
    'https://timesofindia.indiatimes.com/rssfeedstopstories.cms?x=1',
    # 'http://indianexpress.com/feed',
    # 'http://www.thehindu.com/news/national/?service=rss',
    # 'http://www.news18.com/rss/india.xml',
    # 'http://www.firstpost.com/feed/rss',
]


async def fetch(url, session):
    """ Fetch data from an url """
    async with session.get(url) as response:
        return await response.read()


async def get_feed(source, session):
    """ Get the RSS feed from source """
    response = await fetch(source, session)
    parsed = feedparser.parse(response)
    feed = RSSSchema().dump(parsed)  # feed will be and RSS object. Check models.py for reference
    return feed


async def run():
    """ Run the tasks to fetch RSS data from news sources """
    tasks = []
    async with ClientSession() as session:
        for url in list_sources:
            print("fetching from {}".format(url))
            task = asyncio.ensure_future(get_feed(url, session))
            tasks.append(task)
        return await asyncio.gather(*tasks)


async def runner(callback):
    """
    Runs continuously to fetch the latest news from list of various resources

    :param callback: Invoked when the data is fetched and the data is passed
    :return: Never returns
    """
    while True:

        # feed contains the list of all the RSS objects fetched
        feeds = await run()

        # TODO: pass feeds as it is and process/filter them in the special filters
        data = feeds[0]['entries'][1]
        message = "{} {}".format(data['summary'], data['link'])
        print("fetched data: {}".format(message))

        callback_coro = asyncio.coroutine(callback)
        await callback_coro(message)
        await asyncio.sleep(10)


from publish_framework.publishers.news_room import NewsPublisher


async def main():
    """ returns the future for news poller """
    await runner(NewsPublisher.publish)
