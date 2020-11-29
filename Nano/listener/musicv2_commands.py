import validators
import discord
from discord.ext import commands
import os

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

    def __init__(self, client, music_manager: GuildMusicManager):
        self.client = client
        self.music_manager = music_manager
        self.name = "MusicV2"

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
                                  after=lambda error: guild_state.scheduler.on_track_end(source, error, ctx.voice_client))
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

    @join_command.before_invoke
    @play_command.before_invoke
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
