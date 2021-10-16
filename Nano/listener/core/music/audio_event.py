import asyncio
from discord import VoiceClient

from listener.core.music.audio_source import AudioTrack


class AudioEventListener:
    """Audio Event Listener"""

    def on_track_start(self, audio_source):
        pass

    def on_track_end(self, audio_source, error, voice_client):
        pass

    def on_track_error(self, audio_source, error, voice_client):
        pass


class AudioTrackScheduler(AudioEventListener):

    def __init__(self, client):
        self.client = client
        self.queue = []
        self.repeat = False
        self.votes = set()

    async def next_track(self, voice_client: VoiceClient):
        """Play next track"""

        if voice_client is None:
            self.cleanup()
            return

        if not voice_client.is_connected():
            self.cleanup()
            return

        if voice_client.is_connected() and self.queue:
            source = self.queue.pop(0)
            await source.load_source()
            voice_client.play(source, after=lambda error: self.on_track_end(source, error, voice_client))
            self.on_track_start(audio_source=source)

    def cleanup(self):
        """Clears queue"""

        for source in self.queue:
            if source is not None:
                source.cleanup()

        print("Cleaned up queue")

    def on_track_start(self, audio_source):
        return

    def on_track_end(self, audio_source, error, voice_client):
        super().on_track_end(audio_source, error, voice_client)

        if error:
            print("Track ends with error: ", error)
            return

        audio_source.cleanup()

        if self.repeat:
            # Reload source
            future = asyncio.run_coroutine_threadsafe(
                AudioTrack.from_url(audio_source.url, stream=True, requester=audio_source.requester),
                self.client.loop
            )
            sources = future.result()
            if sources:
                self.queue.append(sources.pop(0))

        asyncio.run_coroutine_threadsafe(
            self.next_track(voice_client),
            self.client.loop
        ).result()
        # self.next_track(voice_client)

    def on_track_error(self, audio_source, error, voice_client):
        super().on_track_error(audio_source, error, voice_client)
