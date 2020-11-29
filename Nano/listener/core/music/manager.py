import asyncio

from .audio_event import AudioTrackScheduler


class GuildVoiceState:

    def __init__(self):
        self.volume = 1.0
        self.votes = set()
        self.scheduler = AudioTrackScheduler()
        self.voice_client = None
        self.waiter = None
        self.waiting = False


class GuildMusicManager:

    def __init__(self):
        self.guild_voice_states = {}

    def get_guild_state(self, guild_id) -> GuildVoiceState:
        """Gets Guild's Voice State"""

        if guild_id not in self.guild_voice_states:
            self.guild_voice_states[guild_id] = GuildVoiceState()

        return self.guild_voice_states[guild_id]


