import discord
from discord.ext import commands
from discord.ext.commands import Bot

import praw

import random
import os

reddit = praw.Reddit(
    client_id=os.environ.get('REDDIT_CLIENT_ID'),
    client_secret=os.environ.get('REDDIT_CLIENT_SECRET'),
    user_agent=os.environ.get('REDDIT_USER_AGENT')
)

class RedditListener:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def nba(self, ctx):
        memes_submissions = reddit.subreddit('NBA').hot()
        post_to_pick = random.randint(1, 10)
        for i in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)
        await self.bot.say(submission.url)

    @commands.command(pass_context=True)
    async def memes(self, ctx):
        memes_submissions = list(reddit.subreddit('memes').hot())
        post_to_pick = random.randint(1, 10)
        #for i in range(0, post_to_pick):
        #    submission = next(x for x in memes_submissions if not x.stickied)
        while True:
            submission = random.choice(memes_submissions)
            if not submission.stickied:
                break
        await self.bot.say(submission.url)

    @commands.command(pass_context=True)
    async def rwtf(self, ctx):
        memes_submissions = list(reddit.subreddit('wtf').hot())
        #for i in range(0, post_to_pick):
        #    submission = next(x for x in memes_submissions if not x.stickied)
        while True:
            submission = random.choice(memes_submissions)
            if not submission.stickied and not submission.url.startswith("https://v."):
                break
        
        await self.bot.say(submission.url)
    
def setup(bot):
    bot.add_cog(RedditListener(bot))
    print("Reddit is loaded")
