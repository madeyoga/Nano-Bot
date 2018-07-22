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

startup_extensions = ["Music"]

# DISCORD CLIENT #
bot = commands.Bot(command_prefix='.', description = "General")

# GIPHY #
giphy = safygiphy.Giphy()

# PIXIV #
api = AppPixivAPI()
api.login( str(os.environ.get('PIXIV_MAIL')), str(os.environ.get('PIXIV_PASS')) )

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
    
@bot.command(pass_context=True)
async def pixiv(ctx, *args):
    """ Search img, usage: <prefix>pixiv <args> """
    key = ""
    for word in args:
        key += word
        key += " "
        
    json_result = api.search_illust(key, search_target='partial_match_for_tags')
    if len(json_result.illusts) == 0:
        await bot.say("Couldn't find " + key)
        return
    random_number = random.randint(0, len(json_result.illusts) - 1)
    illust = json_result.illusts[random_number]
    await bot.say("https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(illust.id))

@bot.command(pass_context=True)
async def illust():
    """ returns recommended illust from pixiv """
    json_result = api.illust_recommended(content_type='illust')
    random_number = random.randint(0, len(json_result.illusts) - 1)
    illust = json_result.illusts[random_number]
    await bot.say("https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(illust.id))

@bot.command(pass_context=True)
async def manga():
    """ returns recommended manga from pixiv """ 
    json_result = api.illust_recommended(content_type='manga')
    random_number = random.randint(0, len(json_result.illusts) - 1)
    illust = json_result.illusts[random_number]
    await bot.say("https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(illust.id))

@bot.command(pass_context=True)
async def ranking(ctx, mode : str):
    """ returns ranked img based on mode,'-example ranking' for details """
    json_result = api.illust_ranking(mode='day')
    random_number = random.randint(0, len(json_result.illusts) - 1)
    illust = json_result.illusts[random_number]
    await bot.say("https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(illust.id))
        
@bot.command(pass_context=True)
async def pixivday(ctx):
    """ (Recommended)Pixiv's image based on rank, mode: day """
    json_result = api.illust_ranking('day')
    random_number = random.randint(0, len(json_result.illusts) - 1)
    illust = json_result.illusts[random_number]

    await bot.say("https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(illust.id))

@bot.command(pass_context=True)
async def pixivweek(ctx):
    """ (Recommended)Pixiv's image based on rank, mode: Week """
    json_result = api.illust_ranking('week')
    random_number = random.randint(0, len(json_result.illusts) - 1)
    illust = json_result.illusts[random_number]
    await bot.say("https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(illust.id))

@bot.command(pass_context=True)
async def pixivmonth(ctx):
    """ returns Pixiv's image based on rank, mode: Month """
    json_result = api.illust_ranking('month')
    random_number = random.randint(0, len(json_result.illusts) - 1)
    illust = json_result.illusts[random_number]

    await bot.say("https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(illust.id))

@bot.command(pass_context=True)
async def pixivuser(ctx, user_id):
    """ usage: <prefix>pixivuser <args>, args: user id """
    json_result = api.user_detail(user_id)
    user = json_result.user             #USER
    
    json_result = api.user_illusts(user_id)
    if not len(json_result.illusts) == 0:
        illust = json_result.illusts[0] #ILLUST 
    
    embed = discord.Embed(title="{}'s info".format(user_id), description="Pixiv", color=0x00ff00)
    embed.add_field(name="Name", value=user.name, inline=True)
    embed.add_field(name="User Account", value=user.account, inline=True)
    embed.add_field(name="Request from", value=ctx.message.author, inline=True)
    embed.add_field(name="Link", value="https://www.pixiv.net/member.php?id=" + user_id, inline=True)
    
    if not len(json_result.illusts) == 0:
        await bot.say("User's link\t  : https://www.pixiv.net/member.php?id=" + user_id  + "\nLatest work\t: https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(illust.id))
    else:
        await bot.say("User's link\t  : https://www.pixiv.net/member.php?id=" + user_id)
    

@bot.command(pass_context=True)
async def ping(ctx):
    """Some Text Response"""
    await bot.say(":ping_pong: PIN PON PAN PON!!")

@bot.command(pass_context=True)
async def info(ctx, user: discord.Member):
    """Shows member's Informations"""
    embed = discord.Embed(title="{}'s info".format(user.name), description="Here's what i could find.", color=0x00ff00)
    embed.add_field(name="Name", value=user.name, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Status", value=user.status, inline=True)
    embed.add_field(name="Highest Role", value=user.top_role, inline=True)
    embed.add_field(name="Joined", value=user.joined_at, inline=True)
    embed.set_thumbnail(url=user.avatar_url)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def fact(ctx, user: discord.Member):
    """Some Text Response"""
    if user.name == "SomeLikeItHot" and not user.bot:
        await bot.say("HoT!")
    elif user.bot:
        await bot.say("{} is a bot".format(user.name))
    else:
        await bot.say("{} is gay :eggplant:".format(user.name))

@bot.command(pass_context=True)
async def kick(ctx, user: discord.Member):
    """Kicks member"""
    await bot.say(":boot: Cya, {}. You Loser!".format(user.name))
    await bot.kick(user)

@bot.command(pass_context=True)
async def serverinfo(ctx):
    embed = discord.Embed(title="{}'s info".format(ctx.message.server.name), description="Here's what i could find", color=0x00ff00)
    embed.add_field(name="Name", value=ctx.message.server.name, inline=True)
    embed.add_field(name="ID", value=ctx.message.server.id, inline=True)
    embed.add_field(name="Roles", value=len(ctx.message.server.roles), inline=True)
    embed.add_field(name="Members", value=len(ctx.message.server.members), inline=True)
    embed.set_thumbnail(url=ctx.message.server.icon_url)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def clear(ctx, amount=100):
    channel = ctx.message.channel
    messages = []
    async for message in bot.logs_from(channel, limit=int(amount)):
        messages.append(message)
    await bot.delete_messages(messages)
    await bot.say('Messages deleted')
    
if __name__ == '__main__':
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

bot.run( str(os.environ.get('BOT_TOKEN')) )
