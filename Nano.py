import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
import youtube_dl
from pixivpy3 import *
import safygiphy
import requests
import io
import asyncio
import os
import random
import urllib.request
import urllib.parse
import re
from pathlib import Path

description = """ General """

startup_extensions = ["Music", "Moderation", "Info", "Pixiv"]

# DISCORD CLIENT #
bot = commands.Bot(command_prefix='.', description = "General")

# GIPHY #
giphy = safygiphy.Giphy()

@bot.event
async def on_ready():
    print ('Bot online')
    await bot.change_presence(game=discord.Game(name='.help'))

@bot.event
async def on_member_join(member):
   role = discord.utils.get(member.server.roles, name='New Member')
   await bot.add_roles(member, role)

@bot.command()
async def echo(*args):
    output=""
    for word in args:
        output += word
        output += " "
    await bot.say(output)

@bot.command(pass_context=True)
async def gif(ctx, key : str):
    """ Replies a gif from giphy, <prefix>gif <args> """

    gif_tag = key
    random_gif = giphy.random(tag=str(gif_tag))
    response = requests.get(
        str(random_gif.get("data", {}).get('image_original_url')), stream=True
    )
    if not response:
        await bot.say("couldn't find " + gif_tag)
        return
    await bot.send_file(ctx.message.channel, io.BytesIO(response.raw.read()), filename='video.gif')
    
if __name__ == '__main__':
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

bot.run( str(os.environ.get('BOT_TOKEN')) )
