import asyncio
import discord
from discord.ext import commands
from discord.utils import get
import urllib.request
import urllib.parse
import re
import youtube_dl
import simplejson
import lxml
from lxml import etree
from googleapiclient.discovery import build
from oauth2client.tools import argparser
import os
if not discord.opus.is_loaded():
    
    discord.opus.load_opus('libopus.so')

DEVELOPER_KEY = str(os.environ.get('DEV_KEY'))
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def __init__(self, bot):
        self.bot = bot

class VoiceEntry:
    def __init__(self, message, player):
        self.requester = message.author
        self.channel = message.channel
        self.player = player

    def __str__(self):
        fmt = ' {0.title}'
        duration = self.player.duration
        if duration:
            fmt = fmt + ' [length: {0[0]}m {0[1]}s]'.format(divmod(duration, 60))
        return fmt.format(self.player)

class VoiceState:
    def __init__(self, bot):
        self.current = None
        self.voice = None
        self.bot = bot
        self.play_next_song = asyncio.Event()
        self.songs = asyncio.Queue()
        self.skip_votes = set() # a set of user_ids that voted
        self.audio_player = self.bot.loop.create_task(self.audio_player_task())
        self.list_url = []
        self.list_title = []
        self.active_message = None
        self.queue = []
        
    def is_playing(self):
        if self.voice is None or self.current is None:
            return False

        player = self.current.player
        return not player.is_done()

    @property
    def player(self):
        return self.current.player

    def skip(self):
        self.skip_votes.clear()
        if self.is_playing():
            self.player.stop()

    def toggle_next(self):
        self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

    async def audio_player_task(self):
        while True:
            self.play_next_song.clear()
            self.current = await self.songs.get() ## get queue front 
            embed = discord.Embed(title=':musical_note: Now playing' + str(self.current), color=0x191970)
            await self.bot.send_message(self.current.channel, embed=embed)
            self.current.player.start()
            await self.play_next_song.wait()
            #self.queue.remove(0)

class Music:
    """Voice related commands.
    Works in multiple servers at once.
    """
    def __init__(self, bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, server):
        state = self.voice_states.get(server.id)
        if state is None:
            state = VoiceState(self.bot)
            self.voice_states[server.id] = state
        return state

    async def create_voice_client(self, channel):
        voice = await self.bot.join_voice_channel(channel)
        state = self.get_voice_state(channel.server)
        state.voice = voice

    def __unload(self):
        for state in self.voice_states.values():
            try:
                state.audio_player.cancel()
                if state.voice:
                    self.bot.loop.create_task(state.voice.disconnect())
            except:
                pass

    async def on_reaction_add(self, reaction, user):
        server = reaction.message.server
        state = self.get_voice_state(server)

        if state.active_message and state.active_message.id == reaction.message.id and reaction.emoji == "➕":

            if state.list_title.count == 0:
                await self.bot.send_message(reaction.message.channel, "empty list")
                return True

            for i in range (0, 4):
                if state.list_url.count == 0:
                    break
                state.list_title.pop(0)
                state.list_url.pop(0)

            embed = discord.Embed(title=server.name, description="Playlist", color=0x191970)
            count = 0
            for idx in range(0, 4):
                if len(state.list_url) == count:
                    break
                embed.add_field(name=str(idx + 1) + ". " + state.list_title[idx], value=state.list_url[idx], inline=True)
                count += 1

            await self.bot.delete_message(reaction.message)

            msg = await self.bot.send_message(reaction.message.channel, embed=embed)
            if count == 4:
                await self.bot.add_reaction(msg, emoji="1⃣")
                await self.bot.add_reaction(msg, emoji="2⃣")
                await self.bot.add_reaction(msg, emoji="3⃣")
                await self.bot.add_reaction(msg, emoji="4⃣")
                await self.bot.add_reaction(msg, emoji="➕")
            else:
                for idx in range(0, count):
                    if idx == 0:
                        await self.bot.add_reaction(msg, emoji="1⃣")
                    elif idx == 1:
                        await self.bot.add_reaction(msg, emoji="2⃣")
                    elif idx == 2:
                        await self.bot.add_reaction(msg, emoji="3⃣")
                    elif idx == 3:
                        await self.bot.add_reaction(msg, emoji="4⃣")

            await self.bot.add_reaction(msg, emoji="🎵")
            state.active_message = msg

            return True

        if not state.active_message is None and state.active_message.id == reaction.message.id and not reaction.emoji == "🎵":
            emoji = reaction.emoji
            index = 0
            if emoji == "2⃣":
                index = 1
            elif emoji == "3⃣":
                index = 2
            elif emoji == "4⃣":
                index = 3

            await self.bot.delete_message(reaction.message)
            state.active_message = None
            #await self.bot.send_message(reaction.message.channel, "play #" + str(index + 1))

            summoned_channel = user.voice_channel
            if summoned_channel is None:
                await self.bot.send_message(reaction.message.channel, 'Are you sure you are in a channel?')
                return False

            if state.voice is None:
                state.voice = await self.bot.join_voice_channel(summoned_channel)
            else:
                await state.voice.move_to(summoned_channel)

            try:
                player = await state.voice.create_ytdl_player(state.list_url[index], ytdl_options=None, after=state.toggle_next)
            except Exception as e:
                fmt = 'An error occurred while processing this request: ```py\n{}: {}\n```'
                await self.bot.send_message(reaction.message.channel, fmt.format(type(e).__name__, e))
            else:
                player.volume = 0.6
                entry = VoiceEntry(reaction.message, player)
                state.queue.append(entry)
                embed = discord.Embed(title=':musical_note: Enqueued' + str(entry), color=0x191970)
                await self.bot.send_message(reaction.message.channel, embed=embed)
                await state.songs.put(entry)
            

    @commands.command(pass_context=True, no_pm=True)
    async def s(self, ctx, *args):
        """ Search Song. """
        key = ""
        for word in args:
            key += word
            key += " "
        server = ctx.message.server
        state = self.get_voice_state(server)
        if not state.active_message is None:
            await self.bot.delete_message(state.active_message)
        state.list_url.clear()
        state.list_title.clear()

        count = 0
        embed = discord.Embed(title=server.name, description="Playlist", color=0x191970)
        
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=str(os.environ.get('DEV_KEY')))
        search_response = youtube.search().list(
            q=key,
            part="id,snippet",
            maxResults=25
        ).execute()

        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                #videos.append("%s (%s)" % (search_result["snippet"]["title"], search_result["id"]["videoId"]))
                url = "http://www.youtube.com/watch?v=" + search_result["id"]["videoId"]
                title = search_result["snippet"]["title"]
                
                state.list_url.append(url)
                state.list_title.append(title)

                count += 1
                
        for x in range(0, 4):
            embed.add_field(name=str(x + 1) + ". " + state.list_title[x], value=state.list_url[x], inline=True)


        msg = await self.bot.send_message(ctx.message.channel, embed=embed)
        await self.bot.add_reaction(msg, emoji="1⃣")
        await self.bot.add_reaction(msg, emoji="2⃣")
        await self.bot.add_reaction(msg, emoji="3⃣")
        await self.bot.add_reaction(msg, emoji="4⃣")
        await self.bot.add_reaction(msg, emoji="➕")
        await self.bot.add_reaction(msg, emoji="🎵")
        state.active_message = msg
        
    @commands.command(pass_context=True, no_pm=True)
    async def p(self, ctx, index : int):
        """ Picks Song from Playlist. """
        server = ctx.message.server
        state = self.get_voice_state(server)
        if state.voice is None:
            success = await ctx.invoke(self.summon)
            #await self.bot.say(":notes: Searching :mag: {}".format(song))
            if not success:
                return
        try:
            player = await state.voice.create_ytdl_player(state.list_url[index - 1], ytdl_options=None, after=state.toggle_next)
        except Exception as e:
            fmt = 'An error occurred while processing this request: ```py\n{}: {}\n```'
            await self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))
        else:
            player.volume = 0.6
            entry = VoiceEntry(ctx.message, player)
            #await self.bot.say(':musical_note: Enqueued ' + str(entry))
            embed = discord.Embed(title=':musical_note: Enqueued' + str(entry), color=0x191970)
            state.queue.append(entry)
            await self.bot.say(embed=embed)
            await state.songs.put(entry)
            
    @commands.command(pass_context=True, no_pm=True)
    async def playlist(self, ctx):
        """ Shows playlist """
        server = ctx.message.server
        state = self.get_voice_state(server)
        embed = discord.Embed(title=server.name, description="Playlist", color=0x191970)
        urls = state.list_url
        titles = state.list_title
        count = 0
        for url in urls:
            embed.add_field(name=str(count + 1) + ". " + titles[count], value=url, inline=True)
            count += 1
        await self.bot.say(embed=embed)
        
    @commands.command(pass_context=True, no_pm=True)
    async def join(self, ctx, *, channel : discord.Channel):
        """Joins a voice channel."""
        try:
            await self.create_voice_client(channel)
        except discord.ClientException:
            await self.bot.say('Already in a voice channel...')
        else:
            await self.bot.say('Ready to play audio in **' + channel.name)

    @commands.command(pass_context=True, no_pm=True)
    async def summon(self, ctx):
        """Summons the bot to join your voice channel."""
        summoned_channel = ctx.message.author.voice_channel
        if summoned_channel is None:
            await self.bot.say('Are you sure you are in a channel?')
            return False

        state = self.get_voice_state(ctx.message.server)
        if state.voice is None:
            state.voice = await self.bot.join_voice_channel(summoned_channel)
        else:
            await state.voice.move_to(summoned_channel)

        return True

    @commands.command(pass_context=True, no_pm=True)
    async def play(self, ctx, *, song : str):
        """Plays a song. Search automatically """
        state = self.get_voice_state(ctx.message.server)
        opts = {
            'default_search': 'auto',
            'quiet': True,
        }

        if state.voice is None:
            success = await ctx.invoke(self.summon)
            await self.bot.say(":notes: Searching :mag: {}".format(song))
            if not success:
                return

        try:
            player = await state.voice.create_ytdl_player(song, ytdl_options=opts, after=state.toggle_next)
        except Exception as e:
            fmt = 'An error occurred while processing this request: ```py\n{}: {}\n```'
            await self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))
        else:
            player.volume = 0.6
            entry = VoiceEntry(ctx.message, player)
            #await self.bot.say(':musical_note: Enqueued ' + str(entry))
            embed = discord.Embed(title=':musical_note: Enqueued' + str(entry), color=0x191970)
            state.queue.append(entry)
            await self.bot.send_message(ctx.message.channel, embed=embed)
            await state.songs.put(entry)

    @commands.command(pass_context=True, no_pm=True)
    async def queue(self, ctx):
       """ Songs Queue """
       state = self.get_voice_state(ctx.message.server)
       skip_count = len(state.skip_votes)
       embed = discord.Embed(title='{} [skips: {}/3]'.format(state.current.player.title, skip_count), description=":musical_note: Now playing", color=0x00ff00)
       
       for idx in range(0, len(state.queue)):
            song_duration = "[length: {0[0]}m {0[1]}s]".format(divmod(state.queue[idx].player.duration, 60))
            song_title = "{0}".format(state.queue[idx].player.title)
            embed.add_field(name=song_title + " " + song_duration, value="Requested by " + state.queue[idx].requester.display_name, inline=True)

       await self.bot.say(embed=embed)
        
    @commands.command(pass_context=True, no_pm=True)
    async def volume(self, ctx, value : int):
        """Sets the volume of the currently playing song."""
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.volume = value / 100
            await self.bot.say('Set the volume to {:.0%}'.format(player.volume))
            
    @commands.command(pass_context=True, no_pm=True)
    async def resume(self, ctx):
        """Resumes the currently played song."""
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.resume()
            
    @commands.command(pass_context=True, no_pm=True)
    async def pause(self, ctx):
        """Pause the currently played song."""
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.pause()

    @commands.command(pass_context=True, no_pm=True)
    async def stop(self, ctx):
        """Stops playing audio and leaves the voice channel.
        This also clears the queue.
        """
        server = ctx.message.server
        state = self.get_voice_state(server)
        
        if state.is_playing():
            player = state.player
            player.stop()

        try:
            state.audio_player.cancel()
            del self.voice_states[server.id]
            await state.voice.disconnect()
            await self.bot.say("Cleared the queue and disconnected from voice channel ")
        except:
            pass

    @commands.command(pass_context=True, no_pm=True)
    async def skip(self, ctx):
        """Vote to skip a song. 
        The song requester can automatically skip.
        3 skip votes are needed for the song to be skipped.
        """
        state = self.get_voice_state(ctx.message.server)
        if not state.is_playing():
            await self.bot.say('Not playing any music right now...')
            return

        voter = ctx.message.author
        if voter == state.current.requester:
            await self.bot.say('Requester requested skipping song...')
            state.skip()
        elif voter.id not in state.skip_votes:
            state.skip_votes.add(voter.id)
            total_votes = len(state.skip_votes)
            if total_votes >= 3:
                await self.bot.say('Skip vote passed, skipping song...')
                state.skip()
            else:
                await self.bot.say('Skip vote added, currently at [{}/3]'.format(total_votes))
        else:
            await self.bot.say('You have already voted to skip this song.')

    @commands.command(pass_context=True, no_pm=True)
    async def playing(self, ctx):
        """Shows info about the currently played song."""
        state = self.get_voice_state(ctx.message.server)
        if state.current is None:
            await self.bot.say('Not playing anything.')
        else:
            skip_count = len(state.skip_votes)
            embed = discord.Embed(title=':musical_note: Now playing {} [skips: {}/3]'.format(state.current.player.title, skip_count), color=0x000000)
            embed.add_field(name="Requester", value=state.queue[0].requester.display_name, inline=True)
            embed.add_field(name="Duration", value='[length: {0[0]}m {0[1]}s]'.format(divmod(state.queue[0].player.duration, 60)), inline=True)
            await self.bot.say(embed=embed)
            #':musical_note: Now playing {} [skips: {}/3]'.format(state.current.player.title, skip_count)

def setup(bot):
    bot.add_cog(Music(bot))
    print('Music is loaded')
