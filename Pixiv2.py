from pixiv.pixiv import auth
from pixiv.pixiv.auth import OAuthHandler
from pixiv.pixiv.api import PixivAPI, AppPixivAPI
from pixiv.pixiv.cursor import Cursor, AppCursor
from pixiv.pixiv.utils import PixivDownload

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from threading import Timer,Thread,Event

import asyncio
from itertools import cycle

import io
import requests
import random
import os

auth = OAuthHandler()
auth.login(os.environ.get('PIXIV_MAIL'), os.environ.get('PIXIV_PASS'))
aapi = AppPixivAPI(auth)

class PixivState:
    def __init__(self, bot):
        self.bot = bot
        self.entries = []

class PixivListener:
    def __init__(self, bot, aapi):
        self.bot = bot
        self.pixiv_states = {}
        self.bot.loop.create_task(self.relogin())
        self.aapi = aapi

    async def relogin(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed:
            await asyncio.sleep(900)
            auth = OAuthHandler()
            auth.login("vngla21@gmail.com", "mym12345")
            self.aapi = AppPixivAPI(auth)
            # print("relogin")

    def get_pixiv_state(self, server):
        state = self.pixiv_states.get(server.id)
        if state is None:
            state = PixivState(self.bot)
            self.pixiv_states[server.id] = state
        return state

    def is_number(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    async def on_message(self, message):
        if message.author.bot:
            return
        state = self.get_pixiv_state(message.server)
        if self.is_number(message.content) and state.entries:
            if int(message.content) > 7 or int(message.content) < 1:
                return
            entry = state.entries[int(message.content) - 1]
            detail = self.aapi.user_detail( user_id = entry.user.id )
            msg1 = "**" + detail.user.comment + "**\nRegion: **" + detail.profile.region + "**\n"
            embed = discord.Embed(title="**" + entry.user.name + "**", description=msg1, color=0x9999ff)
            #embed.set_image(url=entry.user.profile_image_urls['medium'])
            embed.add_field(name="**ID**", value=entry.user.id, inline=True)
            embed.add_field(name="**Account**", value="**["+entry.user.account+"](https://www.pixiv.net/member.php?id="+str(entry.user.id)+")**", inline=True)
            embed.add_field(name="**Birthday**", value=detail.profile.birth_day, inline=True)
            embed.add_field(name="**Total Following**", value=str(detail.profile.total_follow_users), inline=True)
            

            msg2 = "Illustrations:\t" + str(detail.profile.total_illusts) + "\nMangas:\t" + str(detail.profile.total_manga) + "\n"
            msg2+= "Novels:\t" + str(detail.profile.total_novels) + "" 
            embed.add_field(name="**Works**", value=msg2, inline=True)
            
            embed.add_field(name="**Total Follower**", value="" + str(detail.profile.total_follower) + "", inline=True)
            if detail.profile.twitter_account and detail.profile.twitter_url:
                embed.add_field(name="**Twitter**", value="**[" + detail.profile.twitter_account + "](" + detail.profile.twitter_url + ")**", inline=True)
            else:
                embed.add_field(name="**Twitter**", value="**", inline=True)                
            embed.add_field(name="**Latest Work**", value="**[" + str(entry.illusts[0].title) + "](https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(entry.illusts[0].id) + ")**", inline=True)
            embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Pixiv_Icon.svg/2000px-Pixiv_Icon.svg.png")
            await self.bot.send_message(message.channel, embed=embed)
            await self.bot.send_message(message.channel, "https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(entry.illusts[0].id) )

    @commands.command(pass_context=True)
    async def pxv_user (self, ctx, *args):
        state = self.get_pixiv_state(ctx.message.server)
        state.entries.clear()
        key = ""
        for word in args:
            key+=word
            key+=" "
        
        entries = self.aapi.search_user( word = key )

        embed = discord.Embed(title="type the `entry number` to see User's detail (entry: 1 - 7)", color=0x9999ff)
        count = 0
        string = ""
        for entry in entries:
            if count == 7:
                break
            state.entries.append(entry)
            string += str(count + 1) + ". **["+entry.user.name+"]("+"https://www.pixiv.net/member.php?id="+str(entry.user.id)+")**, ***" + entry.user.account + "***\n"
            count+=1
        embed.add_field(
                name = "__7 selected artists__", 
                value= string, 
                inline=False
            )
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def illust(self, ctx):
        illusts = self.aapi.illust_recommended()
        illust = random.choice(illusts)
        print("pixiv_recommended_illust: " + illust.title)
        if illust.type == "illust":
            await self.bot.say("`n>translate <text>` to translate\n\nhttps://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(illust.id))

    @commands.command(pass_context=True)
    async def manga(self, ctx):
        illusts = self.aapi.manga_recommended()
        illust = random.choice(illusts)
        print("pixiv_recommended_manga: " + illust.title)
        if illust.type == "manga":
            await self.bot.say("`n>translate <text>` to translate\n\nhttps://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(illust.id))

    @commands.command(pass_context=True)
    async def novel(self, ctx):
        illusts = self.aapi.novel_recommended()
        illust = random.choice(illusts)
        await self.bot.say("`n>translate <text>` to translate\n\nhttps://www.pixiv.net/novel/show.php?id=" + str(illust.id))

    @commands.command(pass_context = True)
    async def pfgo(self, ctx):
        pixvdl = PixivDownload()
        illusts = self.aapi.search_illust( word = "fgo" )
        while True:
            illust = random.choice(illusts)
            if illust.restrict == 0 and illust.type == 'illust' and not "r-18" == illust.tags[0]['name'] and not "R-18" == illust.tags[0]['name']:
               break
            print("R-18, Next")
        print("pixiv_search: " + illust.title)
        if illust.meta_pages:
            await self.bot.say("`n>translate <text>` to translate\nresult has multiple pages\n\nhttps://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(illust.id))
        else:
            message = "**" + illust.user.name + "**\n" + illust.title
            await self.bot.say(message + "\n`n>translate <text>` to translate\n\nhttps://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(illust.id))
    
    @commands.command(pass_context = True)
    async def pxv(self, ctx, *args):
        state = self.get_pixiv_state(ctx.message.server)
        key=""
        for word in args:
            key+=word
            key+=" "
        pixvdl = PixivDownload()
        illusts = self.aapi.search_illust( word = key )
        while True:
            illust = random.choice(illusts)
            if illust.restrict == 0 and illust.type == 'illust' and not "r-18" == illust.tags[0]['name'] and not "R-18" == illust.tags[0]['name']:
               break
            print("R-18, Next")
        print("pixiv_search: " + illust.title)
        if illust.meta_pages:
            #for page in illust.meta_pages:
                #await self.bot.send_file(
                #    ctx.message.channel,
                #    io.BytesIO(pixvdl.get(page['image_urls']['original'])),
                #    filename=illust.title + ".jpg"
                #)
            await self.bot.say("`n>translate <text>` to translate\nresult has multiple pages\n\nhttps://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(illust.id))
            #break
        else:
            message = "**" + illust.user.name + "**\n" + illust.title
            await self.bot.say(message + "\n`n>translate <text>` to translate\n\nhttps://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(illust.id))
            # https://www.pixiv.net/member_illust.php?mode=medium&illust_id=68582289
            # https://www.pixiv.net/member.php?id=10178120
            # illust.id
            # illust.user.id
            #embed = discord.Embed(
            #        title="**Pixiv**",
            #        color=0x0000ff
            #    )
            #embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Pixiv_Icon.svg/2000px-Pixiv_Icon.svg.png")
            #embed.add_field(name="User's Link", value="**[" + illust.user.name + "](https://www.pixiv.net/member.php?id=" + str(illust.user.id) + ")**")
            #embed.add_field(name="Illust's Link", value="**[" + illust.title + "](https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(illust.id) + ")**")
            #await self.bot.say(embed=embed)
            #await self.bot.send_file(
            #    ctx.message.channel,
            #    io.BytesIO(pixvdl.get(illust.meta_single_page['original_image_url'])),
            #    filename=illust.title + ".jpg"
            #)
        
def setup(bot):
    bot.add_cog(PixivListener(bot, aapi))
    print("new PixivListener is loaded")
