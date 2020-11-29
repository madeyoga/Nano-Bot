import asyncio
import os

import aiohttp
import discord

from listener.core.client import NanoClient
from listener.musicv2_commands import MusicV2Cog


def get_memory_config():
    intents = discord.Intents(messages=True, guilds=True)

    intents.voice_states = True
    intents.typing = False
    intents.presences = False
    intents.members = False
    intents.bans = False
    intents.integrations = False
    intents.invites = False
    intents.dm_messages = False
    intents.guild_reactions = False

    return intents


async def main():
    global loop

    # ENVIRONMENTS
    nano_token = os.environ['NR_TOKEN']

    # Configure client
    intents = get_memory_config()
    client = NanoClient(command_prefix='n!', intents=intents)
    client.remove_command('help')

    # Add Cogs/Commands
    startup_extensions = [
        'listener.general_commands',
        'listener.image_commands',
    ]
    # for extension in startup_extensions:
    #     try:
    #         client.load_extension(extension)
    #     except Exception as e:
    #         exc = '{}: {}'.format(type(e).__name__, e)
    #         print('Failed to load extension {}\n{}'.format(extension, exc))

    session = aiohttp.ClientSession()
    # client.add_cog(Music(client, session))
    client.add_cog(MusicV2Cog(client=client))
    print('MusicListener is Loaded')

    # Run Bot
    try:
        loop.run_until_complete(await client.start(nano_token))
    except Exception as e:
        await session.close()
        print('Session closed.')
        print(e)


loop = asyncio.get_event_loop()

loop.run_until_complete(main())
