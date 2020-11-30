import asyncio
from discord import Member, VoiceState, VoiceChannel, VoiceClient
from discord.ext import commands

from listener.core.music.manager import GuildMusicManager


class MemberVoiceEventManager:

    async def on_voice_join(self, self_voice_client: VoiceClient, member: Member, voice_state_after: VoiceState):
        pass

    async def on_voice_leave(self, self_voice_client: VoiceClient, member: Member, voice_state_before: VoiceState):
        pass

    async def on_voice_move(self, self_voice_client: VoiceClient, member: Member, before: VoiceState, after: VoiceState):
        pass


class MemberVoiceListener(commands.Cog, MemberVoiceEventManager):
    """Member voice listener to update voice state"""

    def __init__(self, client, music_manager: GuildMusicManager):
        super().__init__()
        self.name = "MemberVoiceListener"
        self.client = client
        self.music_manager = music_manager

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):
        """Check when member changes their VoiceState"""

        # Ignore if member is bot
        if member.bot:
            return

        # Ignore if self voice client is None
        self_voice_client = member.guild.voice_client
        if self_voice_client is None:
            return

        # Ignore if event is not move/join/leave
        if before.channel is not None and after.channel is not None and before.channel.id == after.channel.id:
            return

        # Ignore if move event is from other voice channel to other voice channel
        if before.channel is not None and before.channel.id != self_voice_client.channel.id and \
           after.channel is not None and after.channel.id != self_voice_client.channel.id:
            # print("event from other channel", before.channel.id, self_voice_client.channel.id,
            #       before.channel, self_voice_client.channel)
            return
        # Member leave other voice channel
        elif before.channel is not None and before.channel.id != self_voice_client.channel.id and after.channel is None:
            # print("event from other channel", before.channel, self_voice_client.channel)
            return
        # Member join other voice channel
        elif before.channel is None and after.channel is not None and after.channel.id != self_voice_client.channel.id:
            # print("event from other channel", before.channel, self_voice_client.channel)
            return

        # Event is from and to self client voice channel
        else:

            # A member leaves self_client's voice channel
            if after.channel is None:
                await self.on_voice_leave(self_voice_client, member, before)
            # A member join self_client's voice channel
            elif after.channel.id == self_voice_client.channel.id:
                await self.on_voice_join(self_voice_client, member, after)
            # A member moves to other voice channel, from self_client's voice channel
            else:
                await self.on_voice_leave(self_voice_client, member, before)

        return

    async def on_voice_join(self, self_voice_client: VoiceClient, member: Member, voice_state_after: VoiceState):

        guild_state = self.music_manager.get_guild_state(member.guild.id)

        # If a user join self client voice channel, and voice client is waiting
        if guild_state.waiting or guild_state.waiter is not None:
            # Resume
            guild_state.waiter.cancel()
            guild_state.waiting = False

            self_voice_client.resume()

            # print("Cancel waiter and resume playing")
            return

        return await super().on_voice_join(self_voice_client, member, voice_state_after)

    async def on_voice_leave(self, self_voice_client: VoiceClient, member: Member, voice_state_before: VoiceState):

        # If self client voice is empty.
        if not self.there_is_user_in_voice(voice_state_before.channel):
            guild_state = self.music_manager.get_guild_state(member.guild.id)

            self_voice_client.pause()

            guild_state.waiter = asyncio.ensure_future(self.wait_for_user(self_voice_client, member.guild))
            guild_state.waiting = True

            # print("Pause and wait for user")
            return

        return await super().on_voice_leave(self_voice_client, member, voice_state_before)

    async def on_voice_move(self, self_voice_client: VoiceClient, member: Member,
                            before: VoiceState, after: VoiceState):
        return await super().on_voice_move(self_voice_client, member, before, after)

    async def wait_for_user(self, voice_client, guild):

        await asyncio.sleep(10)

        if voice_client.source is not None:
            voice_client.source.cleanup()

        await voice_client.disconnect()

        del self.music_manager.guild_voice_states[guild.id]

    @staticmethod
    def there_is_user_in_voice(channel: VoiceChannel):
        """Check voice channel members"""

        for member in channel.members:
            if not member.bot:
                return True

        return False
