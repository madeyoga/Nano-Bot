import discord
from discord.ext import commands

class NanoContext(commands.Context):
    @property
    def secret(self):
        return 'this is my secret'

class NanoClient(commands.Bot):
    def __init__(self, name='Nano', id='536892183404478483',
        owner_id='213866895806300161', command_prefix='do.'):
        super(NanoClient, self).__init__(command_prefix)
        self.name = name
        self.id = id
        self.owner_id = owner_id
        self.command_prefix = command_prefix

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

#     async def on_message(self, message):
#         if message.author.bot:
#             return
#         # print('Message from {0.author}: {0.content}'.format(message))
#         ctx = await self.get_context(message, cls=NanoContext)
#         await self.invoke(ctx)
