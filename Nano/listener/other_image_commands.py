from discord.ext import commands
from .core.base import BaseImageCog
from .core.subreddit import other_subreddits
from random import choice
from random import randint


class OtherImageCog(BaseImageCog):

    def __init__(self, reddit_client):
        super().__init__()
        self.name = "Image Commands"
        self.load_pools(other_subreddits)
        self.reddit = reddit_client

    @commands.is_owner()
    @commands.command(name="reload_other_pool")
    async def reload_other_pool_command(self, ctx):
        self.load_pools(other_subreddits)
        await ctx.send(":white_check_mark: | Reloaded, other image pools!")

    @commands.cooldown(1, 1, commands.BucketType.guild)
    @commands.command(name="memes", aliases=["meme"])
    async def memes_command(self, ctx):
        """Get random post from  /r/memes

        **Usage**
        ```
        n>memes
        ```
        """

        submission = choice(self.pools["MEMES"])

        await self.reply_context(ctx=ctx, submission=submission)

    @commands.cooldown(1, 1, commands.BucketType.guild)
    @commands.command(name="wtf", aliases=["rwtf"])
    async def wtf_command(self, ctx):
        """Get random post from  /r/wtf

        **Usage**
        ```
        n>wtf
        ```
        """

        submission = choice(self.pools["WTF"])

        await self.reply_context(ctx=ctx, submission=submission)

    @commands.cooldown(1, 1, commands.BucketType.guild)
    @commands.command(name="dank")
    async def dank_command(self, ctx):
        """Get random post from  /r/dankmemes

        **Usage**
        ```
        n>dank
        ```
        """

        submission = choice(self.pools["DANKMEMES"])

        await self.reply_context(ctx=ctx, submission=submission)

    @commands.cooldown(1, 1, commands.BucketType.guild)
    @commands.command(name="reddit_search", aliases=["reddit", "r", "r/"])
    async def reddit_search_command(self, ctx, *keywords):
        """Search post from reddit

        **Usage**
        ```
        n>reddit <keywords>
        n>reddit_search <keywords>
        n>r <keywords>
        n>r/ <keywords>
        ```
        """

        keywords = ' '.join(keywords)

        subreddit = await self.reddit.subreddit("all")

        random_index = randint(0, 24)
        current_index = 0
        async for submission in subreddit.search(keywords, limit=10):
            if current_index == random_index:
                await ctx.send(submission.url)
                break
            current_index += 1
