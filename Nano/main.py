import os
import asyncio
import aiohttp
import discord
from listener.core.client import NanoClient as Client
from listener.music_commands import Music

def configure_memory_usage():
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

async def main(loop):

    startup_extensions = [
        'listener.general_commands',
        'listener.image_commands',
    ]

    intents = configure_memory_usage()

    client = Client(command_prefix='n>', intents=intents)

    client.remove_command('help')

    for extension in startup_extensions:
        try:
            client.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
    
    session = aiohttp.ClientSession()
    client.add_cog(Music(client, session))
    print('MusicListener is Loaded')

    try:
        loop.run_until_complete(await client.start(os.environ['BOT_TOKEN']))
    except:
        await session.close()
        print('Session closed.')

loop = asyncio.get_event_loop()

loop.run_until_complete(main(loop))