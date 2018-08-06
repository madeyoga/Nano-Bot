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
import aiohttp
from pathlib import Path

startup_extensions = ["Moderation", "Info", "gag", "Translator"]

# DISCORD CLIENT #
bot = commands.Bot(command_prefix='.', description = "General")
bot.remove_command('help')

dbltoken = str(os.environ.get('DBL_TOKEN'))
url = "https://discordbots.org/api/bots/458298539517411328/stats"
headers = {"Authorization" : dbltoken}

# GIPHY #
giphy = safygiphy.Giphy()

@bot.event
async def on_ready():
    print ('Bot online')
    await bot.change_presence(game=discord.Game(name='.help'))
    
    payload = {"server_count"  : len(bot.servers)}
    async with aiohttp.ClientSession() as aioclient:
        await aioclient.post(url, data=payload, headers=headers)
            
@bot.event
async def on_server_join(server):
    payload = {"server_count"  : len(bot.servers)}
    async with aiohttp.ClientSession() as aioclient:
        await aioclient.post(url, data=payload, headers=headers)
        
@bot.event
async def on_server_remove(server):
    payload = {"server_count"  : len(bot.servers)}
    async with aiohttp.ClientSession() as aioclient:
        await aioclient.post(url, data=payload, headers=headers)

@bot.command(pass_context=True)
async def help(ctx, cmd = None):
    if ctx.message.author.bot:
        return
    if cmd is None or cmd == "":
        author = ctx.message.author
        embed = discord.Embed(
            color=0x0000ff
            )
        embed.set_author(name=".help <command>, to get command's detail")
        
        embed.add_field(name="Info", value=".info, .ping, .serverinfo", inline=False)
        embed.add_field(name="Moderation", value=".clear, .kick", inline=False)
        embed.add_field(name="Music, use !help to see more", value="!p, !play, !np, !playlist, !queue, !s, !skip, !leave, !summon, !volume, !music_prefix", inline=False)
        embed.add_field(name="9gag's sections", value=".anime, .comic, .cosplay, .kpop, .savage, .wtf", inline=False)
        embed.add_field(name="Translator", value=".translate, .translate_to", inline=False)
        embed.add_field(name="No Category", value=".help, .echo, .gif, .support", inline=False)
        embed.add_field(name="Full Info", value="https://discordbots.org/bot/458298539517411328", inline=False)
        await bot.say(embed=embed)
    else:
        example = "usage: "
        if cmd == "info":
            example+=".info @user"
        elif cmd == "ping":
            example+=".ping"
        elif cmd == "serverinfo":
            example+=".serverinfo"
        elif cmd == "clear":
            example+=".clear / .clear 100"
        elif cmd == "kick":
            example+=""
        elif cmd == "join":
            example+=".join <server's name>"
        elif cmd == "p":
            example+="!p 4 ,picks index 4 from playlist"
        elif cmd == "pause":
            example+=".pause"
        elif cmd == "play":
            example+="!play music"
        elif cmd == "np":
            example+="!playing ,shows currently playing song's info"
        elif cmd == "s":
            example+="!s anime ,search anime from youtube\nresults will be stored to playlist"
        elif cmd == "skip":
            example+="!skip\n"
            example+="requester can immediately skips the song"
        elif cmd == "playlist":
            example+="!playlist"
        elif cmd == "anime":
            example+=".anime"
        elif cmd == "wtf":
            example+=".wtf"
        elif cmd == "savage":
            example+=".savage"
        elif cmd == "kpop":
            example+=".kpop"
        elif cmd == "comic":
            example+=".comic"
        elif cmd == "cosplay":
            example+=".cosplay"
        elif cmd == "help":
            example+=".help"
        elif cmd == "echo":
            example+=".echo hello world"
        await bot.say(example)

@bot.command(pass_context=True)
async def echo(ctx, *args):
    if ctx.message.author.bot:
        return
    output=""
    for word in args:
        output += word
        output += " "
    await bot.say(output)

@bot.command(pass_context=True)
async def support(ctx):
    if ctx.message.author.bot:
        return
    await bot.say("https://discordbots.org/bot/458298539517411328/vote")
    
@bot.command(pass_context=True)
async def gif(ctx, key : str):
    """ Replies a gif from giphy, <prefix>gif <args> """
    if ctx.message.author.bot:
        return
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
