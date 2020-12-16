import discord
from discord.ext import commands


class PixivCog(commands.Cog):
    """Pixiv command listener cogs"""

    def __init__(self, client):
        self.client = client
