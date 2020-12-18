import asyncio
import os
import json

import aiohttp
import discord
from discord.ext import commands
from pixivpy_async import PixivClient
from ytpy import YoutubeClient
import asyncpraw
from listener.anime_image_commands import AnimeImageCog
from listener.core.client import NanoClient
from listener.core.music.manager import GuildMusicManager
from listener.error_listener import ErrorListener
from listener.fgo_image_commands import FgoImageCog
from listener.general_commands import GeneralCog
from listener.help_commands import HelpCog
from listener.musicv2_commands import MusicV2Cog
from listener.other_image_commands import OtherImageCog
from listener.owner_commands import OwnerCog
from listener.pixiv_commands import PixivCog
from listener.voice_listener import MemberVoiceListener

prefixes = ["n>"]
default_prefix = "n>"
server_prefixes = {}


def load_server_prefixes():
    global server_prefixes

    with open("prefixes.json") as f:
        server_prefixes = json.load(f)


def save_server_prefixes():
    global server_prefixes

    with open('prefixes.json', 'w') as fp:
        json.dump(server_prefixes, fp, indent=2)


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


def get_prefix(bot, message):
    guild_id = str(message.guild.id)

    if guild_id in server_prefixes:
        return commands.when_mentioned_or(*server_prefixes[guild_id] + prefixes)(bot, message)

    return commands.when_mentioned_or(*prefixes)(bot, message)


async def main():
    global loop

    # ENVIRONMENTS
    nano_token = os.environ['BOT_TOKEN']

    # Load server settings
    load_server_prefixes()

    # Configure client
    intents = get_memory_config()
    client = NanoClient(command_prefix=get_prefix, intents=intents)
    client.remove_command('help')

    # Load Dependencies for DI
    session = aiohttp.ClientSession()
    youtube_client = YoutubeClient(session)
    music_manager = GuildMusicManager(client=client)
    reddit_client = asyncpraw.Reddit(client_id=os.environ['REDDIT_CLIENT_ID'],
                                     client_secret=os.environ['REDDIT_CLIENT_SECRET'],
                                     user_agent=os.environ['REDDIT_USER_AGENT'])

    pixiv_client = PixivClient()

    # Load command Cogs
    cogs = [
        GeneralCog(client=client, server_prefixes=server_prefixes),
        MusicV2Cog(client=client, music_manager=music_manager, youtube_client=youtube_client),
        MemberVoiceListener(client=client, music_manager=music_manager),
        FgoImageCog(),
        AnimeImageCog(),
        OtherImageCog(reddit_client),
        ErrorListener(),
        # PixivCog(client, pixiv_client),
        OwnerCog()
    ]

    for command_cog in cogs:
        client.add_cog(command_cog)
        print(command_cog.name, "is Loaded")

    client.add_cog(HelpCog(client=client, server_prefixes=server_prefixes))
    print("Help is Loaded")

    # Run Bot
    try:
        loop.run_until_complete(await client.start(nano_token))
    except Exception as e:
        print(e)

    save_server_prefixes()
    print('Saved prefixes')
    await session.close()
    await pixiv_client.close()
    print('Session closed.')

loop = asyncio.get_event_loop()

loop.run_until_complete(main())
