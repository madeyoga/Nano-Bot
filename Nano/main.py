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

async def create_aiohttp_client():
    return aiohttp.ClientSession()

async def close_session(session):
    await session.close()

def main(session):

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
    
    client.add_cog(Music(client, session))
    print('MusicListener is Loaded')

    client.run(os.environ['BOT_TOKEN'])

loop = asyncio.new_event_loop()

session = loop.run_until_complete(create_aiohttp_client())

main(session)

loop.run_until_complete(close_session(session))

loop.close()