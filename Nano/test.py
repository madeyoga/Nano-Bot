import os
import asyncio
from pixivpy_async import AppPixivAPI, PixivClient, PixivAPI


async def test_pixivpy_async_app_api():
    client = PixivClient(env=True)
    aapi = AppPixivAPI(client=client.start())

    # conn = aiohttp.TCPConnector(limit_per_host=30)
    # session = aiohttp.ClientSession(
    #     connector=conn,
    #     timeout=aiohttp.ClientTimeout(total=10),
    #     trust_env=True,
    # )
    # client.client = session

    username, password = os.environ['PIXIV_USERNAME'], os.environ['PIXIV_PASS']
    
    # For App Pixiv API
    await aapi.login(username, password)

    res = await aapi.illust_ranking("day")
    illusts = res.get("illusts")
    print(len(illusts), illusts[0])

    await client.close()


async def test_pixivpy_async_public_api():
    papi = PixivAPI()
    
    username, password = os.environ['PIXIV_MAIL'], os.environ['PIXIV_PASS']
    
    # For App Pixiv API
    await papi.login(username, password)

    res = await papi.ranking("illust", "day", 1)
    print(res)

loop = asyncio.get_event_loop()
loop.run_until_complete(test_pixivpy_async_app_api())
