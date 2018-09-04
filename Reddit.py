import discord
from discord.ext import commands
from discord.ext.commands import Bot

import praw
import random

from ImageCore import *

subreddits = Subreddits()

class RedditListener:
    def __init__(self, bot):
        self.bot = bot
        self.reddit = Reddit()


    @commands.command(pass_context=True)
    async def memes(self, ctx):
        submission = self.reddit.get_submission(subreddits.MEMES)
        embed = discord.Embed(
            color = 0x0000ff
        )
        embed.set_image(url=submission.url)
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def rwtf(self, ctx):
        submission = self.reddit.get_submission(subreddits.WTF)
        embed = discord.Embed(
            color = 0x0000ff
        )
        embed.set_image(url=submission.url)
        await self.bot.say(embed=embed)
    
    @commands.command(pass_context=True)
    async def dank(self, ctx):
        submission = self.reddit.get_submission(subreddits.DANKMEMES)
        embed = discord.Embed(
            color = 0x0000ff
        )
        embed.set_image(url=submission.url)
        await self.bot.say(embed=embed)
    
    @commands.command(pass_context=True)
    async def aniwallp(self, ctx):
        submission = self.reddit.get_submission(subreddits.ANIMEWALLPAPER)
        embed = discord.Embed(
            color = 0x0000ff
        )
        embed.set_image(url=submission.url)
        await self.bot.say(embed=embed)
    
    @commands.command(pass_context=True)
    async def animeme(self, ctx):
        submission = self.reddit.get_submission(subreddits.ANIMEMES)
        embed = discord.Embed(
            color = 0x0000ff
        )
        embed.set_image(url=submission.url)
        await self.bot.say(embed=embed)
    
    @commands.command(pass_context=True)
    async def waifu(self, ctx):
        submission = self.reddit.get_submission(subreddits.WAIFU)
        embed = discord.Embed(
            color = 0x0000ff
        )
        embed.set_image(url=submission.url)
        await self.bot.say(embed=embed)
    
    @commands.command(pass_context=True)
    async def fgo(self, ctx):
        submission = self.reddit.get_submission(subreddits.GRANDORDER)
        embed = discord.Embed(
            color = 0x0000ff
        )
        embed.set_image(url=submission.url)
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def fgoart(self, ctx):
        submission = self.reddit.get_submission(subreddits.FGOFANART)
        embed = discord.Embed(
            color = 0x0000ff
        )
        embed.set_image(url=submission.url)
        await self.bot.say(embed=embed)
    
    @commands.command(pass_context=True)
    async def fgoart(self, ctx):
        submission = self.reddit.get_submission(subreddits.FGOFANART)
        embed = discord.Embed(
            color = 0x0000ff
        )
        embed.set_image(url=submission.url)
        await self.bot.say(embed=embed)
    
    @commands.command(pass_context=True)
    async def tsun(self, ctx):
        submission = self.reddit.get_submission(subreddits.TSUNDERES)
        embed = discord.Embed(
            color = 0x0000ff
        )
        embed.set_image(url=submission.url)
        await self.bot.say(embed=embed)
    
    @commands.command(pass_context=True)
    async def anime(self, ctx):
        submission = self.reddit.get_submission(subreddits.ANIME)
        embed = discord.Embed(
            color = 0x0000ff
        )
        embed.set_image(url=submission.url)
        await self.bot.say(embed=embed)
    
    @commands.command(pass_context=True)
    async def scathach(self, ctx):
        submission = self.reddit.get_submission(subreddits.SCATHACH)
        embed = discord.Embed(
            color = 0x0000ff
        )
        embed.set_image(url=submission.url)
        await self.bot.say(embed=embed)
    
    @commands.command(pass_context=True)
    async def moescape(self, ctx):
        submission = self.reddit.get_submission(subreddits.MOESCAPE)
        embed = discord.Embed(
            color = 0x0000ff
        )
        embed.set_image(url=submission.url)
        await self.bot.say(embed=embed)
    
def setup(bot):
    bot.add_cog(RedditListener(bot))
    print("Reddit is loaded")
