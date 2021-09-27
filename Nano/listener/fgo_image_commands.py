from discord.ext import commands
import json

from .core.submission import embed_submission
from .core.subreddit import fgo_subreddits
from random import choice
import os


class FgoImageCog(commands.Cog):

    def __init__(self):
        self.name = "FGO"
        self.fgo_pools = {}
        self.load_pools()

    def load_pools(self):
        for key, subreddit_name in fgo_subreddits.items():
            cache_filepath = f"listener/cache/{subreddit_name}.json"
            if not os.path.exists(cache_filepath):
                continue
            with open(cache_filepath, 'r') as json_file:
                self.fgo_pools[key] = json.loads(json_file.read())

    @staticmethod
    async def reply_context(ctx, submission):
        if submission.get('post_hint') == 'image':
            await ctx.send(embed=embed_submission(submission))
        else:
            await ctx.send(submission.get('url'))

    @commands.is_owner()
    @commands.command(name="reload_fgo_pool")
    async def reload_fgo_pool_command(self, ctx):
        self.fgo_pools.clear()
        self.load_pools()

        await ctx.send(":white_check_mark: | Reloaded, fgo pools!")

    @commands.cooldown(1, 1, commands.BucketType.guild)
    @commands.command(name="fgo")
    async def fgo_command(self, ctx):
        """Get random post from  /r/GrandOrder

        **Usage**
        ```
        n>fgo
        ```
        """

        submission = choice(self.fgo_pools["GRANDORDER"])
        await self.reply_context(ctx=ctx, submission=submission)

    @commands.cooldown(1, 1, commands.BucketType.guild)
    @commands.command(name="fgoart")
    async def fgo_fan_art_command(self, ctx):
        """Get random post from  /r/FGOfanart

        **Usage**
        ```
        n>fgoart
        ```
        """

        submission = choice(self.fgo_pools["FGOFANART"])
        await self.reply_context(ctx=ctx, submission=submission)

    @commands.cooldown(1, 1, commands.BucketType.guild)
    @commands.command(name="saber")
    async def saber_command(self, ctx):
        """Get random post from  /r/Saber

        **Usage**
        ```
        n>saber
        ```
        """

        submission = choice(self.fgo_pools["SABER"])

        await self.reply_context(ctx=ctx, submission=submission)

    @commands.cooldown(1, 1, commands.BucketType.guild)
    @commands.command(name="raikou")
    async def raikou_command(self, ctx):
        """Get random post from  /r/MamaRaikou

        **Usage**
        ```
        n>raikou
        ```
        """

        if ctx.channel.is_nsfw():
            submission = choice(self.fgo_pools["MAMARAIKOU"])
            await self.reply_context(ctx=ctx, submission=submission)
        else:
            await ctx.send(":x: | This command can be used only in nsfw channel.")

    @commands.cooldown(1, 1, commands.BucketType.guild)
    @commands.command(name="scathach")
    async def scathach_command(self, ctx):
        """Get random post from  /r/scathach

        **Usage**
        ```
        n>scathach
        ```
        """

        submission = choice(self.fgo_pools["SCATHACH"])
        await self.reply_context(ctx=ctx, submission=submission)

    @commands.cooldown(1, 1, commands.BucketType.guild)
    @commands.command(name="illya", aliases=["illyasviel"])
    async def illyasviel_command(self, ctx):
        """Get random post from  /r/Illya

        **Usage**
        ```
        n>illya
        ```
        """

        submission = choice(self.fgo_pools["ILLYASVIEL"])
        await self.reply_context(ctx=ctx, submission=submission)

    @commands.cooldown(1, 1, commands.BucketType.guild)
    @commands.command(name="fgocomics", aliases=["fgo_comics"])
    async def fgo_comics_command(self, ctx):
        """Get random comics from  /r/FGOcomics

        **Usage**
        ```
        n>fgocomics
        ```
        """

        submission = choice(self.fgo_pools["FGOCOMICS"])
        await self.reply_context(ctx=ctx, submission=submission)

    @commands.cooldown(1, 1, commands.BucketType.guild)
    @commands.command(name="rin")
    async def rin_command(self, ctx):
        """Get random comics from  /r/OneTrueTohsaka

        **Usage**
        ```
        n>rin
        ```
        """

        submission = choice(self.fgo_pools["ONETRUETOHSAKA"])
        await self.reply_context(ctx=ctx, submission=submission)

    @commands.cooldown(1, 1, commands.BucketType.guild)
    @commands.command(name="jeanne")
    async def jeanne_command(self, ctx):
        """Get random comics from  /r/ChurchOfJeanne

        **Usage**
        ```
        n>jeanne
        ```
        """
        submission = choice(self.fgo_pools["CHURCHOFJEANNE"])
        await self.reply_context(ctx=ctx, submission=submission)
