from random import choice
import asyncio
import discord
from discord.ext import commands
from pixivpy_async import PixivClient, AppPixivAPI
import os
from listener.core.client import NanoClient


class PixivCog(commands.Cog):
    """Pixiv command listener cogs

    mode: [day, week, month, day_male, day_female, week_original, week_rookie, day_manga]
    """

    def __init__(self, client: NanoClient, pixiv_client: PixivClient()):
        self.name = "Pixiv"
        self.client = client
        self.aapi = AppPixivAPI(client=pixiv_client.start())
        self.day_pool = {}
        self.day_male_pool = {}
        self.day_female_pool = {}
        self.base_url = 'https://www.pixiv.net/en/artworks/'
        asyncio.ensure_future(self.load_pools_async())

    async def load_pools_async(self):
        username, password = os.environ['PIXIV_USERNAME'], os.environ['PIXIV_PASS']
        await self.aapi.login(username, password)
        self.day_pool = await self.aapi.illust_ranking("day")
        self.day_male_pool = await self.aapi.illust_ranking("day_male")
        self.day_female_pool = await self.aapi.illust_ranking("day_female")

    @commands.is_owner()
    @commands.command(name="reload_pixiv_pool")
    async def reload_pixiv_pool_command(self, ctx):
        self.day_pool.clear()
        self.day_male_pool.clear()
        self.day_female_pool.clear()
        await self.load_pools_async()

        await ctx.send(":white_check_mark: | Reloaded, pixiv pools")

    @commands.command(name="pxday")
    async def day_command(self, ctx):
        """Get random post from pixiv daily rankings

        **Usage**
        ```
        n>pxday
        ```
        """
        random_post = choice(self.day_pool.get("illusts"))
        await ctx.send(f'{self.base_url}{random_post.get("id")}')
        return

    @commands.command(name="pxdaymale")
    async def day_male(self, ctx):
        """Get random post from pixiv daily rankings (popular among male)

        **Usage**
        ```
        n>pxdaymale
        ```
        """
        random_post = choice(self.day_male_pool.get("illusts"))
        await ctx.send(f'{self.base_url}{random_post.get("id")}')
        return

    @commands.command(name="pxdayfemale")
    async def day_female(self, ctx):
        """Get random post from pixiv daily rankings (popular among female)

        **Usage**
        ```
        n>pxdayfemale
        ```
        """
        random_post = choice(self.day_female_pool.get("illusts"))
        await ctx.send(f'{self.base_url}{random_post.get("id")}')
        return
