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
        """
            checkin nano-bot's ping
        """
        if ctx.message.author.bot:
            return
        channel = ctx.message.channel
        now = time.perf_counter()
        await self.bot.send_typing(channel)
        then = time.perf_counter()
        embed = discord.Embed(title="Nano-bot's ping", color=0x000000)
        embed.add_field(name=":hourglass_flowing_sand:{}ms".format(round((then-now)*1000)), value="ping test")
        await self.bot.say(embed=embed)
        
    @commands.command(pass_context=True)
    async def info(self, ctx, user: discord.Member):
        if ctx.message.author.bot:
            return
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
        if ctx.message.author.bot:
            return
        if user.name == "SomeLikeItHot" and not user.bot:
            await self.bot.say("HoT!")
        elif user.bot:
            await self.bot.say("{} is a bot".format(user.name))
        else:
            await self.bot.say("{} is gay :eggplant:".format(user.name))

    @commands.command(pass_context=True)
    async def serverinfo(self, ctx):
        if ctx.message.author.bot:
            return
        embed = discord.Embed(title="{}'s info".format(ctx.message.server.name), description="Here's what i could find", color=0x00ff00)
        embed.add_field(name="Name", value=ctx.message.server.name, inline=True)
        embed.add_field(name="ID", value=ctx.message.server.id, inline=True)
        embed.add_field(name="Roles", value=len(ctx.message.server.roles), inline=True)
        embed.add_field(name="Members", value=len(ctx.message.server.members), inline=True)
        embed.set_thumbnail(url=ctx.message.server.icon_url)
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def servers(self, ctx):
        if ctx.message.author.id == "213866895806300161":
            servers = self.bot.servers
            embed = discord.Embed(
                color=0x0000ff
            )
            embed.set_author(name="Servers")
            count=0
            for server in servers:
                count+=1
                members=""
                #for member in server.members:
                #    members+=member.name + ","
                embed.add_field(name=str(count) + ". " + server.name, value=len(server.members), inline=True)
            await self.bot.say(embed=embed)
        else:
            embed = discord.Embed(color=0x0000ff)
            embed.set_image(url="http://i.imgur.com/aF13v7A.gif")
            await bot.say(embed=embed)
    
def setup(bot):
    bot.add_cog(Info(bot))
    print('Info is loaded')

        
