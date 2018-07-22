import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio


def __init__(self, bot):
    self.bot = bot

class Moderation:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def kick(self, ctx, user: discord.Member):
        """ Kicks member """
        await self.bot.say(":boot: Bye~ Have a good daay~, {}.".format(user.name))
        await self.bot.kick(user)

    @commands.command(pass_context=True)
    async def clear(self, ctx, amount=100):
        """ clear messages, default: 100 messages """
        channel = ctx.message.channel
        messages=[]
        async for message in self.bot.logs_from(channel, limit=int(amount)):
            messages.append(message)

        await self.bot.delete_messages(messages)
        
        await self.bot.say('Messages deleted')

        
def setup(bot):
    bot.add_cog(Moderation(bot))
    print('Moderation is loaded')
