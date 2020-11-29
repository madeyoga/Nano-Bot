import discord
from discord.ext import commands

commands_string = """
**Music**
`play`, `p`, `search`, `s`, `volume`, `queue`, `q`, `skip`, `stop`, `now_playing`, `now_play`, `nowplay`, `np`, `pause`, `resume`, `repeat`, `loop`, `shuffle`

**FGO Image**
`fgo` `fgoart` `scathach` `raikou` `saber` `abby`

**Image**
`dank` `anime` `animeme` `anime9` `waifu` `tsun` `aniwallp` `moescape` `rwtf`

**Reddit Image Search**
aliases: `reddit` `r/` `reddit_search`
usage: 
```n>reddit <keywords>```
"""


class GeneralCog(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.name = "General"

    # @commands.command()
    # async def help(self, ctx):
    #     embed = discord.Embed(
    #         title="Nano-bot's Command List",
    #         colour=discord.Colour(value=11735575).orange()
    #     )
    #     embed.add_field(
    #         name=":tools: **Support Dev**",
    #         value="Feedback/Report bug, [Join Nano Support Server](https://discord.gg/Y8sB4ay)\nDon't forget to **["
    #               "Vote](https://discordbots.org/bot/458298539517411328/vote)** Nano-Bot :hearts: "
    #     )
    #     embed.add_field(
    #         name=":books: **Commands** | Prefix: **n>**",
    #         value=commands_string,
    #         inline=False
    #     )
    #     nano_bot = self.client.get_user(self.client.user.id)
    #     embed.set_thumbnail(url=nano_bot.avatar_url)
    #     await ctx.send(embed=embed)

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
