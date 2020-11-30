import discord
from discord.ext import commands


class GeneralCog(commands.Cog):

    def __init__(self, client, server_prefixes: dict):
        self.client = client
        self.name = "General"
        self.server_prefixes = server_prefixes

    @commands.command(name="set_prefix")
    async def set_prefix(self, ctx, arg):
        """Set guild's custom prefix"""

        if arg.startswith('n>'):
            await ctx.send(":x: | Cannot use prefix that starts with `n>`.")
            return

        guild_id = str(ctx.guild.id)
        self.server_prefixes[guild_id] = [arg]

        await ctx.send(f":white_check_mark: | Custom prefix has been set to {arg}, you can test it using {arg}help")

    @commands.command()
    async def secret(self, ctx):
        await ctx.send(ctx.secret)

    @commands.command()
    async def ping(self, ctx):
        latency = "%.0fms" % (self.client.latency * 100)
        embed = discord.Embed(
            title="{}-bot's Latency'".format(self.client.name),
            type='rich',
            description=":hourglass_flowing_sand:" + latency,
            colour=discord.Colour(value=11735575).orange()
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def say(self, ctx, *args):
        await ctx.send(" ".join(args))

    @commands.command()
    async def set_status(self, ctx, *args):
        if ctx.message.author.id != ctx.owner_id:
            return
        await self.client.change_presence(activity=discord.Game(" ".join(args)))

    @commands.command(aliases=['avatar'])
    async def ava(self, ctx, *args):
        """Response mentioned user's avatar"""

        if len(ctx.message.mentions) <= 0:
            await ctx.send("Please @mention the user")
            return
        mentioned_user = ctx.message.mentions[0]
        embed = discord.Embed(title=mentioned_user.name, type="rich")
        embed.set_image(url=mentioned_user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=["vcmute", "mute", "mute_all"])
    async def vc_mute(self, ctx):
        vc = ctx.author.voice.channel

        for member in vc.members:
            await member.edit(mute=True)


def setup(client):
    client.add_cog(GeneralCog(client))
    print('GeneralListener is Loaded')
