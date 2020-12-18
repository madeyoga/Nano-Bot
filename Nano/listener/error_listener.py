from discord.ext import commands
import traceback


class ErrorListener(commands.Cog):

    def __init__(self):
        self.name = "Error Listener"

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.NSFWChannelRequired):
            return await ctx.send(":x: | This command is potentially nsfw and can only be used in nsfw channel.")
        if isinstance(error, commands.errors.CommandOnCooldown):
            return await ctx.send(":x: | You are on cooldown. Try again in 1 second")
        else:
            print(error)
