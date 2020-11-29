import validators
import discord
from discord.ext import commands
import os

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
        """Join user's voice channel"""

        connected_channel_name = ctx.channel.name
        await ctx.send(f":white_check_mark: | Joined :loud_sound: `{connected_channel_name}`")

    @commands.command(name="leave", aliases=["stop"])
    async def leave_command(self, ctx):
        """Stop playing and leaves voice channel"""

        ctx.voice_client.source.cleanup()
        await ctx.voice_client.disconnect()

        del self.music_manager.guild_voice_states[ctx.guild.id]

    @commands.command(name="play", aliases=["p"])
    async def play_command(self, ctx, *, query):
        """Load and play source from given query
        query can be a url or keywords
        """

        guild_state = self.music_manager.get_guild_state(ctx.guild.id)
        await self.load_and_play(ctx=ctx, query=query, guild_state=guild_state)

    @commands.command(name="search", aliases=["s"])
    async def search_command(self, ctx, *, args):
        """Search and select song to play"""

        print(args)
        videos = await self.youtube_client.search(args, max_results=5)
        print(videos)

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
            search_list += f"[{i+1}]. **[{video['title']}]({video_url})** [{video['duration']}]\n"

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
        except:
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
        """Show now playing song"""

        if ctx.voice_client is None or ctx.voice_client.source is None:
            await ctx.send(":x: | Not playing anything")
        else:
            await ctx.send(f":musical_note: Now playing **{ctx.voice_client.source.title}**")

    @commands.command(name="queue", aliases=["sq"])
    async def show_queue_command(self, ctx):
        """Show queue entries"""
        return

    @join_command.before_invoke
    @play_command.before_invoke
    @search_command.before_invoke
    async def ensure_voice(self, ctx):
        """Do this before invoke commands"""

        # If bot voice is not connected to voice
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.author.voice is None:
            await ctx.send("You are not connected to a voice channel.")
            raise commands.CommandError("Author not connected to a voice channel.")

    @staticmethod
    async def load_and_play(ctx, query, guild_state):
        # If valid url
        if validators.url(query):
            sources = await AudioTrack.from_url(query, stream=True)
        else:
            sources = await AudioTrack.from_keywords(query, stream=True)

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

            await ctx.send(":musical_note: Added to queue **" + source.title + "**")

        # If voice client is playing
        else:
            guild_state.scheduler.queue += sources

            if len(sources) == 1:
                await ctx.send(":musical_note: Added to queue **" + sources[0].title + "**")
                return

            await ctx.send(f":musical_note: Added to queue **{len(sources)} entries**")

    @staticmethod
    def check(m, request_channel, request_author):
        try:  # '/^*[0-9][0-9 ]*$/'
            picked_entry_number = int(m.content)
            return m.channel == request_channel and m.author == request_author
        except:
            return False
