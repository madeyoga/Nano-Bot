from pixivpy_async import *


class PixivService:

    def __init__(self, client: PixivClient):
        self.pixiv_client = client
        self.aapi = AppPixivAPI(client=client.start())
        self.papi = PixivAPI()

    async def search_illust(self, query):
        return await self.aapi.search_illust("FGO", search_target='partial_match_for_tags')
