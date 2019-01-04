import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
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

from datetime import date

startup_extensions = ["Moderation", "Info", "gag", "Translator", "Reddit"]

commands_string = "**Image**\n`memes` `dank` `anime` `animeme` `anime9` `waifu` `tsun` `aniwallp` `moescape` `fgo` `fgoart` `cosplay` `comic` `rwtf` `wtf` `kpop` `savage`\n"
commands_string += "**Music**\n`play` `p` `search` `s` `s_limit` `volume` `skip` `pause` `resume` `leave` `repeat` `np` `queue`\n"
commands_string += "**Manage**\n`kick` `add_role` `ban` `c_text` `c_voice` `c_category` `rm_role`\n"
commands_string += "**Translate**\n`translate` `translate_to` `translate_from`\n"
commands_string += "**Other**\n`lenny` `flip` `avatar` `eva`"

# DISCORD CLIENT #
bot = commands.Bot(command_prefix='n>', description = "General")
bot.remove_command('help')

dbltoken = str(os.environ.get('DBL_TOKEN'))
url = "https://discordbots.org/api/bots/458298539517411328/stats"
headers = {"Authorization" : dbltoken}

# GIPHY #
giphy = safygiphy.Giphy()

@bot.event
async def on_ready():
    print ('Bot online')
    await bot.change_presence(game=discord.Game(name='n>help'))
    
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
    embed = discord.Embed(
        color=0x0000ff
    )

    embed.add_field(
        name=":bookmark: **Check wiki for Commands guide**\n",
        value="[Wiki](https://github.com/MadeYoga/Nano-Bot/wiki/Welcome-to-the-Nano-Bot-wiki!)\n[Change Log](https://github.com/MadeYoga/Nano-Bot/blob/master/changelog.md)",
        inline=False
        )
    embed.add_field(
        name=":tools: **Support Dev**",
        value="Report bug, [Join Nano Support Server](https://discord.gg/Y8sB4ay)\nDon't forget to **[Vote](https://discordbots.org/bot/458298539517411328/vote)** Nano-Bot :hearts:"
        )
    embed.add_field(
        name=":books: **Commands** | Prefix: **n>**",
        value=commands_string,
        inline=False
        )
    embed.set_footer(text="Nano-bot " + str(date.today()))
    embed.set_thumbnail(url=bot.user.avatar_url)
    await bot.say(embed=embed)

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

@bot.command()
async def eva(*args):
    expression = ""
    for arg in args:
        expression += arg + " "

    try:
        res = eval(expression)
    except e:
        await bot.say("invalid syntax")
    await bot.say(res)

if __name__ == '__main__':
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

bot.run( str(os.environ.get('BOT_TOKEN')) )
