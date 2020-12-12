import discord
from discord.ext import commands
import os
import aiohttp


class NanoContext(commands.Context):
    @property
    def secret(self):
        return 'this is my secret'


class NanoClient(commands.AutoShardedBot):
    def __init__(self, name='Nano', id=536892183404478483,
                 owner_id=213866895806300161, command_prefix='do.', intents=None):
        super(NanoClient, self).__init__(command_prefix=command_prefix,
                                         max_messages=None,
                                         intents=intents,
                                         chunk_guilds_at_startup=False)
        self.name = name
        self.id = id
        self.owner_id = owner_id
        self.command_prefix = command_prefix

        # Discord Bot List updates.
        self.dbl_token = os.environ['DBL_TOKEN']
        self.BASE_URL = "https://discordbots.org/api/bots/458298539517411328/stats"
        self.headers = {"Authorization": self.dbl_token}

    async def update_status_on_dbl(self):
        payload = {"server_count": len(super(NanoClient, self).guilds)}
        async with aiohttp.ClientSession() as session:
            await session.post(self.BASE_URL, data=payload, headers=self.headers)

    async def on_ready(self):
        status_message = discord.Game("n>help")
        await super(NanoClient, self).change_presence(status=discord.Status.online, activity=status_message)
        await self.update_status_on_dbl()
        print("Logged in as {}".format(super(NanoClient, self).user))

    async def on_guild_join(self, guild):
        """Updates DBL when client joins a guild"""
        await self.update_status_on_dbl()

    async def on_guild_leave(self, guild):
        """Updates DBL when client leaves a guild"""
        await self.update_status_on_dbl()

    async def on_message(self, message):
        if message.author.bot:
            return
        await self.invoke(await self.get_context(message, cls=NanoContext))
