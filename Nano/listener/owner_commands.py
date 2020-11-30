from discord.ext import commands


class OwnerCog(commands.Cog):

    def __init__(self):
        self.name = "Owner"

    @commands.command(name="shutdown")
    @commands.is_owner()
    async def shutdown(self, ctx):
        """Owner only"""

        await ctx.send("Shutting down...")
        await ctx.bot.logout()
