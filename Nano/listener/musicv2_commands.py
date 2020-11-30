import validators
import discord
from discord.ext import commands
import os
import random
from ytpy import YoutubeClient

from listener.core.custom.embed import CustomEmbed
from listener.core.music.audio_source import AudioTrack
from listener.core.music.manager import GuildMusicManager

# Check os. If not windows, then try load libopus
if os.name != 'nt':
    if not discord.opus.is_loaded():
        discord.opus.load_opus("libopus.so.1")


class MusicV2Cog(commands.Cog):
    """
    Reimplementation of Music Commands.
    """

    def __init__(self, client, music_manager: GuildMusicManager, youtube_client: YoutubeClient):
        self.client = client
        self.music_manager = music_manager
        self.name = "MusicV2"
        self.youtube_client = youtube_client

    @commands.command(name="join", aliases=["summon"])
    async def join_command(self, ctx):
        """Join user's voice channel

        **Usage**
        ```
        n>join
        n>summon
        """

        connected_channel_name = ctx.channel.name
        await ctx.send(f":white_check_mark: | Joined :loud_sound: `{connected_channel_name}`")

    @commands.command(name="leave", aliases=["stop"])
    async def leave_command(self, ctx):
        """Stop playing and leaves voice channel

        **Usage**
        ```
        n>leave
        n>stop
        ```
        """

        if ctx.voice_client.is_playing():
            ctx.voice_client.source.cleanup()
            ctx.voice_client.stop()

        await ctx.voice_client.disconnect()

        del self.music_manager.guild_voice_states[ctx.guild.id]

    @commands.command(name="play", aliases=["p"])
    async def play_command(self, ctx, *, query):
        """Load and play source from given query
        query can be an url or keywords

        **Usage**
        ```
        n>play hello world
        n>play https://someurl/
        ```
        """

        guild_state = self.music_manager.get_guild_state(ctx.guild.id)
        await self.load_and_play(ctx=ctx, query=query, guild_state=guild_state)

    @commands.command(name="search", aliases=["s"])
    async def search_command(self, ctx, *, args):
        """Search and select song to play

        **Usage**
        ```py
        n>search hello world

        # reply song index
        1
        ```
        """

        videos = await self.youtube_client.search(args, max_results=5)

        embed = CustomEmbed()
        embed.set_author(name="Song Selection | Reply the song number to continue",
                         icon_url=self.client.user.avatar_url,
                         url=self.client.user.avatar_url)

        embed.set_thumbnail(url=videos[0]["thumbnails"][0])

        search_list = ""
        base_url = "https://www.youtube.com/watch?v="
        for i, video in enumerate(videos):
            video_url = base_url + video['id']
            videos[i]["url"] = video_url
            search_list += f"[{i + 1}]. **[{video['title']}]({video_url})** [{video['duration']}]\n"

        embed.add_field(name=f"Search result for `{args}`", value=search_list, inline=False)

        embed.set_footer(text="Song selection | Reply the number to continue",
                         icon_url=self.client.user.avatar_url)

        embedded_list = await ctx.send(embed=embed)

        request_channel = ctx.message.channel
        request_author = ctx.author

        try:
            message = await self.client.wait_for('message',
                                                 check=lambda m: self.check(m, request_channel, request_author),
                                                 timeout=10.0)
        except TimeoutError as e:
            # TIMEOUT ERROR EXCEPTION
            await embedded_list.delete()
            return

        selected_index = int(message.content)
        if 0 < selected_index < 6:
            selected_song = videos[selected_index - 1]
            guild_state = self.music_manager.get_guild_state(ctx.guild.id)
            await self.load_and_play(ctx, selected_song['url'], guild_state=guild_state)
        else:
            await embedded_list.delete()
            await ctx.send(":x: | Index out of range. Valid range: `1 - 5`")

    @commands.command(name="now_play", aliases=["np"])
    async def now_play_command(self, ctx):
        """Show now playing song

        **Usage**
        ```
        n>now_play
        n>np
        ```
        """

        if ctx.voice_client is None or ctx.voice_client.source is None:
            await ctx.send(":x: | Not playing anything")
        else:
            await ctx.send(f":musical_note: Now playing **{ctx.voice_client.source.title}**")

    @commands.command(name="queue", aliases=["q"])
    async def show_queue_command(self, ctx):
        """Show queue entries

        **Usage**
        ```
        n>queue
        n>q
        ```
        """

        embed = CustomEmbed()
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.title = f"{ctx.guild.name}'s Queue"
        embed.set_thumbnail(url=ctx.guild.icon)

        guild_state = self.music_manager.get_guild_state(ctx.guild.id)

        entries = "*Empty*"
        if guild_state.scheduler.queue:
            entries = ""
            for i, entry in enumerate(guild_state.scheduler.queue):
                entries += f"[{i + 1}]. **{entry.title}** [{entry.duration}]\n"
                if i >= 6:
                    break
        embed.add_field(name=":musical_note: Top 7 Songs in Queue", value=entries, inline=False)

        if guild_state.scheduler.queue:
            embed.set_thumbnail(url=guild_state.scheduler.queue[0].thumbnail)
        else:
            embed.set_thumbnail(url=ctx.guild.icon_url)

        await ctx.send(embed=embed)

    @commands.command(name="repeat", aliases= ["loop"])
    async def repeat_command(self, ctx):
        """Re-enqueue the song after it finished playing

        **Usage**
        ```
        n>repeat
        n>loop
        ```
        """

        guild_state = self.music_manager.get_guild_state(ctx.guild.id)
        if guild_state.scheduler.repeat:
            guild_state.scheduler.repeat = False
            await ctx.message.add_reaction('\u21AA')
        else:
            guild_state.scheduler.repeat = True
            await ctx.message.add_reaction('\u21AA')

    @commands.command(name="pause")
    async def pause_command(self, ctx):
        """Pause or resume current song

        **Usage**
        ```
        n>pause
        ```
        """

        if ctx.voice_client is not None:
            if ctx.voice_client.is_paused():
                ctx.voice_client.resume()
                await ctx.message.add_reaction('\u25B6')
            elif ctx.voice_client.is_playing():
                ctx.voice_client.pause()
                await ctx.message.add_reaction('\u23F8')
            else:
                await ctx.send(":x: | Not playing anything")
        else:
            await ctx.send(":x: | Not playing anything")

    @commands.command(name="resume")
    async def resume_command(self, ctx):
        """Resume paused song, if any

        **Usage**
        ```
        n>resume
        ```
        """

        if ctx.voice_client is not None and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.message.add_reaction('\u25B6')

    @commands.command(name="shuffle", aliases=["shuffle_queue"])
    async def shuffle_command(self, ctx):
        """Shuffles songs in queue

        **Usage**
        ```
        n>shuffle
        n>shuffle_queue
        ```
        """

        guild_state = self.music_manager.get_guild_state(ctx.guild.id)
        if guild_state.scheduler.queue:
            random.shuffle(guild_state.scheduler.queue)
            await self.show_queue_command(ctx=ctx)
        else:
            await ctx.send(":x: | Queue is empty.")

    @commands.command(name="skip")
    async def skip_command(self, ctx):
        """Skips current playing song
        Only song requester can skip the song

        **Usage**
        ```
        n>skip
        ```
        """

        if ctx.voice_client.source is None:
            await ctx.send(":x: | Not playing anything")
            return

        # guild_state = self.music_manager.get_guild_state(ctx.guild.id)
        if ctx.author.id == ctx.voice_client.source.requester.id:
            ctx.voice_client.stop()
            await ctx.message.add_reaction('\u23ED')
        return

    @join_command.before_invoke
    @leave_command.before_invoke
    @play_command.before_invoke
    @search_command.before_invoke
    @repeat_command.before_invoke
    @skip_command.before_invoke
    async def ensure_voice(self, ctx):
        """Do this before invoke commands"""

        # If bot is not connected to voice
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.author.voice is None:
            await ctx.send("You are not connected to a voice channel.")
            raise commands.CommandError("Author not connected to a voice channel.")
        else:
            await ctx.author.voice.channel.connect()

    @staticmethod
    async def load_and_play(ctx, query, guild_state):
        # If valid url
        if validators.url(query):
            sources = await AudioTrack.from_url(query, stream=True, requester=ctx.author)
        else:
            sources = await AudioTrack.from_keywords(query, stream=True, requester=ctx.author)

        if not ctx.voice_client.is_playing():

            if not sources:
                await ctx.send(":x: | Cannot sources load from `" + query + "`")

            source = sources.pop(0)

            ctx.voice_client.play(source,
                                  after=lambda error: guild_state.scheduler.on_track_end(source, error,
                                                                                         ctx.voice_client))
            guild_state.scheduler.on_track_start(audio_source=source)

            # If there is more sources
            if sources:
                guild_state.scheduler.queue += sources
                await ctx.send(":musical_note: Added to queue **" + source.title + f"** and {len(sources)} entries")
                return

            await ctx.send(":musical_note: Added to queue **" + source.title + "** : **" + source.uploader + "**")

        # If voice client is playing
        else:
            guild_state.scheduler.queue += sources

            if len(sources) == 1:
                await ctx.send(f":musical_note: Added to queue **{sources[0].title}** : **{sources[0].uploader}**")
                return

            await ctx.send(f":musical_note: Added to queue **{len(sources)} entries**")

    @staticmethod
    def check(m, request_channel, request_author):
        try:  # '/^*[0-9][0-9 ]*$/'
            int(m.content)
            return m.channel == request_channel and m.author == request_author
        except ValueError as e:
            return False
