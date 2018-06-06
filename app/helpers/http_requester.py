import asyncio
from aiohttp import ClientSession

__all__ = ['make_http_request']


async def get(session, url, data=None, json=True):
    """
    make an async get request to the url with data as body
    :param (ClientSession) session:
    :param (string) url: url to post data to
    :param (dict/binary coded string) data: data to be posted
    :param (bool) json: if the data is Json formal
    :return:
    """
    if json:
        async with session.get(url, json=data) as response:
            return await response.text()
    else:
        raise NotImplementedError("Please send Json data")
        # async with session.get(url, data=data) as response:
        #     return await response.text()


async def post(session, url, data=None, json=True):
    """
    make an async post request to the url with data as body
    :param (ClientSession) session:
    :param (string) url: url to post data to
    :param (dict/binary coded string) data: data to be posted
    :param (bool) json: if the data is Json formal
    :return:
    """
    if json:
        async with session.post(url, json=data) as response:
            return await response.text()
    else:
        raise NotImplementedError("Please send Json data")
        # async with session.post(url, data=data) as response:
        #     return await response.text()


async def make_http_request(url, data=None, json=True, method="GET"):
    async with ClientSession() as session:
        print("fetching from {}".format(url))

        if method.upper() == "GET":
            requester = get
        elif method.upper() == "POST":
            requester = post
        else:
            raise NotImplementedError("Method not implemented")

        return await requester(session=session, url=url, data=data, json=json)


if __name__ == "__main__":
    # for testing this module
    url = "http://example.com"
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(make_http_request(url))
    response = loop.run_until_complete(future)
    print(response)
