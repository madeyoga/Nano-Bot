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

startup_extensions = ["Music", "Moderation", "Info", "gag"]

# DISCORD CLIENT #
bot = commands.Bot(command_prefix='.', description = "General")
bot.remove_command('help')

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

@bot.command(pass_context=True)
async def help(ctx, cmd = None):
    if cmd is None or cmd == "":
        author = ctx.message.author
        embed = discord.Embed(
            color=0x0000ff
            )
        embed.set_author(name=".help <command>")
        
        embed.add_field(name="Info", value="info, ping, serverinfo", inline=False)
        embed.add_field(name="Moderation", value="clear, kick", inline=False)
        embed.add_field(name="Music", value="join, p, pause, play, playing, playlist, queue, resume, s, skip, stop, summon, volume", inline=False)
        embed.add_field(name="9gag", value="anime, comic, cosplay, kpop, savage, wtf", inline=False)
        embed.add_field(name="No Category", value="help, echo, gif, status", inline=False)
        
        await bot.say(embed=embed)
    else:
        await bot.say("'i promise i will add this feature soon..' - dev")
    
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

@bot.command(pass_context=True)
async def status(ctx, *args):
    if ctx.message.author.id == "213866895806300161":
        stat=""
        for word in args:
            stat+=word
            stat+=" "
        await bot.change_presence(game=discord.Game(name=stat))
        await bot.say("Hay Master! i have changed my status to " + stat)
    else:
        embed = discord.Embed(color=0x0000ff)
        embed.set_image(url="http://i.imgur.com/aF13v7A.gif")
        await bot.say(embed=embed)

if __name__ == '__main__':
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

bot.run( str(os.environ.get('BOT_TOKEN')) )
