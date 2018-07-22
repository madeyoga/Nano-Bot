import discord
from discord.ext import commands
from discord.ext.commands import Bot
import time
import datetime
import asyncio

def __init__(self, bot):
    self.bot = bot

class Info:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def ping(self, ctx):
        channel = ctx.message.channel
        now = time.perf_counter()
        await self.bot.send_typing(channel)
        then = time.perf_counter()
        embed = discord.Embed(title="{}'s ping".format(ctx.message.author.name), color=0x000000)
        embed.add_field(name=":hourglass_flowing_sand:{}ms".format(round((then-now)*1000)), value="ping test")
        #await self.bot.say("ping: {}ms".format(round((then-now)*1000)))
        await self.bot.say(embed=embed)
        
    @commands.command(pass_context=True)
    async def info(self, ctx, user: discord.Member):
        embed = discord.Embed(title="{}'s info".format(user.name), description="Here's what i could find.", color=0x00ff00)
        embed.add_field(name="Name", value=user.name, inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Status", value=user.status, inline=True)
        embed.add_field(name="Highest Role", value=user.top_role, inline=True)
        embed.add_field(name="Joined", value=user.joined_at, inline=True)
        embed.set_thumbnail(url=user.avatar_url)
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def fact(self, ctx, user: discord.Member):
        """Some Text Response"""
        if user.name == "SomeLikeItHot" and not user.bot:
            await self.bot.say("HoT!")
        elif user.bot:
            await self.bot.say("{} is a bot".format(user.name))
        else:
            await self.bot.say("{} is gay :eggplant:".format(user.name))

    @commands.command(pass_context=True)
    async def serverinfo(self, ctx):
        embed = discord.Embed(title="{}'s info".format(ctx.message.server.name), description="Here's what i could find", color=0x00ff00)
        embed.add_field(name="Name", value=ctx.message.server.name, inline=True)
        embed.add_field(name="ID", value=ctx.message.server.id, inline=True)
        embed.add_field(name="Roles", value=len(ctx.message.server.roles), inline=True)
        embed.add_field(name="Members", value=len(ctx.message.server.members), inline=True)
        embed.set_thumbnail(url=ctx.message.server.icon_url)
        await self.bot.say(embed=embed)

def setup(bot):
    bot.add_cog(Info(bot))
    print('Info is loaded')

        
