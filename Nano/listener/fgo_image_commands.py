from discord.ext import commands
import json
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

        if submission['over_18'] is False:
            await ctx.send(submission.get('url'))

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

        await ctx.send(submission.get('url'))

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

        await ctx.send(submission.get('url'))

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
            await ctx.send(submission.get('url'))
        else:
            await ctx.send(":x: | This command is potentially nsfw and can only be used in nsfw channel.")

    @commands.cooldown(1, 1, commands.BucketType.guild)
    @commands.command(name="scathach")
    async def scathach_command(self, ctx):
        """Get random post from  /r/scathach

        **Usage**
        ```
        n>scathach
        ```
        """

        if ctx.channel.is_nsfw():
            submission = choice(self.fgo_pools["SCATHACH"])
            await ctx.send(submission.get('url'))
        else:
            await ctx.send(":x: | This command is potentially nsfw and can only be used in nsfw channel.")

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

        await ctx.send(submission.get('url'))

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

        await ctx.send(submission.get('url'))
