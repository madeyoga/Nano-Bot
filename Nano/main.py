import asyncio
import json
import os

import asyncpraw
import discord
from discord.ext import commands

from listener.anime_image_commands import AnimeImageCog
from listener.core.client import NanoClient
from listener.error_listener import ErrorListener
from listener.fgo_image_commands import FgoImageCog
from listener.general_commands import GeneralCog
from listener.help_commands import HelpCog
from listener.other_image_commands import OtherImageCog
from listener.owner_commands import OwnerCog


def load_server_prefixes() -> dict:
    server_prefixes = {}
    with open("prefixes.json") as f:
        server_prefixes = json.load(f)
    return server_prefixes


def save_server_prefixes(server_prefixes) -> None:

    with open('prefixes.json', 'w') as fp:
        json.dump(server_prefixes, fp, indent=2)


def get_memory_config():
    intents = discord.Intents(messages=True, guilds=True)

    intents.voice_states = False
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


async def main(loop, server_prefixes, prefixes, default_prefix):

    # ENVIRONMENTS
    nano_token = os.environ['NR_TOKEN']

    # Configure client
    intents = get_memory_config()
    client = NanoClient(command_prefix=get_prefix, intents=intents)
    client.remove_command('help')

    # Load Dependencies
    reddit_client = asyncpraw.Reddit(client_id=os.environ['REDDIT_CLIENT_ID'],
                                        client_secret=os.environ['REDDIT_CLIENT_SECRET'],
                                        user_agent=os.environ['REDDIT_USER_AGENT'])

    # Load command Cogs
    cogs = [
        GeneralCog(client=client, server_prefixes=server_prefixes),
        AnimeImageCog(),
        FgoImageCog(),
        OtherImageCog(reddit_client),
        ErrorListener(),
        OwnerCog()
    ]

    for command_cog in cogs:
        client.add_cog(command_cog)
        print(command_cog.name, "is Loaded")

    client.add_cog(HelpCog(client=client, server_prefixes=server_prefixes))
    print("Help is Loaded")

    # Run Bot
    await client.start(nano_token)

    save_server_prefixes(server_prefixes)


server_prefixes = load_server_prefixes()
prefixes = ["n>"]
default_prefix = "n>"

loop = asyncio.get_event_loop()

loop.run_until_complete(main(loop, server_prefixes, prefixes, default_prefix))
