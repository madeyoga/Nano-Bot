import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import requests
from pixivpy3 import *
import random
import io
import os
import urllib.request
import urllib.parse
import re
from pathlib import Path

PIXIV_MAIL = str(os.environ.get('PIXIV_MAIL'))
PIXIV_PASS = str(os.environ.get('PIXIV_PASS')

# PIXIV #
api = AppPixivAPI()
api.login(PIXIV_MAIL, PIXIV_PASS)

class Pixiv:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def pixiv(self, ctx, *args):
        """ Search img, usage: <prefix>pixiv <args> """
        key = ""
        for word in args:
            key += word
            key += " "
        
        json_result = api.search_illust(key, search_target='partial_match_for_tags')
        if len(json_result.illusts) == 0:
            await bot.say("Couldn't find " + key)
            return
        random_number = random.randint(0, len(json_result.illusts) - 1)
        illust = json_result.illusts[random_number]
        await self.bot.say("https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(illust.id))

    @commands.command(pass_context=True)
    async def illust(self):
        """ recommended illust from pixiv """
        json_result = api.illust_recommended(content_type='illust')
        random_number = random.randint(0, len(json_result.illusts) - 1)
        illust = json_result.illusts[random_number]
        await self.bot.say("https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(illust.id))

    @commands.command(pass_context=True)
    async def manga(self):
        """ recommended manga from pixiv """ 
        json_result = api.illust_recommended(content_type='manga')
        random_number = random.randint(0, len(json_result.illusts) - 1)
        illust = json_result.illusts[random_number]
        await self.bot.say("https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(illust.id))

    @commands.command(pass_context=True)
    async def ranking(self, ctx, mode : str):
        """ returns ranked img based on mode,'-example ranking' for details """
        json_result = api.illust_ranking(mode='day')
        random_number = random.randint(0, len(json_result.illusts) - 1)
        illust = json_result.illusts[random_number]
        await self.bot.say("https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(illust.id))
        
    @commands.command(pass_context=True)
    async def pixivday(self, ctx):
        """ (Recommended)Pixiv's image based on rank, mode: day """
        json_result = api.illust_ranking('day')
        random_number = random.randint(0, len(json_result.illusts) - 1)
        illust = json_result.illusts[random_number]

        await self.bot.say("https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(illust.id))

    @commands.command(pass_context=True)
    async def pixivweek(self, ctx):
        """ (Recommended)Pixiv's image based on rank, mode: Week """
        json_result = api.illust_ranking('week')
        random_number = random.randint(0, len(json_result.illusts) - 1)
        illust = json_result.illusts[random_number]
        await self.bot.say("https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(illust.id))

    @commands.command(pass_context=True)
    async def pixivmonth(self, ctx):
        """ returns Pixiv's image based on rank, mode: Month """
        json_result = api.illust_ranking('month')
        random_number = random.randint(0, len(json_result.illusts) - 1)
        illust = json_result.illusts[random_number]

        await self.bot.say("https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(illust.id))

    @commands.command(pass_context=True)
    async def pixivuser(self, ctx, user_id):
        """ usage: <prefix>pixivuser <args>, args: user id """
        json_result = api.user_detail(user_id)
        user = json_result.user             #USER
    
        json_result = api.user_illusts(user_id)
        if not len(json_result.illusts) == 0:
            illust = json_result.illusts[0] #ILLUST 
    
        embed = discord.Embed(title="{}'s info".format(user_id), description="Pixiv", color=0x00ff00)
        embed.add_field(name="Name", value=user.name, inline=True)
        embed.add_field(name="User Account", value=user.account, inline=True)
        embed.add_field(name="Request from", value=ctx.message.author, inline=True)
        embed.add_field(name="Link", value="https://www.pixiv.net/member.php?id=" + user_id, inline=True)
    
        if not len(json_result.illusts) == 0:
            await self.bot.say("User's link\t  : https://www.pixiv.net/member.php?id=" + user_id  + "\nLatest work\t: https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(illust.id))
        else:
            await self.bot.say("User's link\t  : https://www.pixiv.net/member.php?id=" + user_id)
 
def setup(bot):
    bot.add_cog(Pixiv(bot))
    print('Pixiv is loaded')
