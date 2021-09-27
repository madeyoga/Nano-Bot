import discord
import yt_dlp as youtube_dl
import asyncio

from discord import User

from .utilities import parse_duration

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'before_options': '-re -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn -nostats -loglevel 0 -use_wallclock_as_timestamps 1'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class AudioTrack(discord.AudioSource):
    def __init__(self, original, *, data, requester: User = ""):
        self.original = original

        self.title = data.get('title', 'None')
        self.uploader = data.get('uploader', 'None')
        self.url = data.get('webpage_url', 'None')
        self.source_url = data.get('url', None)
        self.duration = parse_duration(int(data.get('duration', 0)))
        self.thumbnail = data.get('thumbnail', 'https://gallery.autodesk.com/assets/default%20tile%20thumbnail'
                                               '-dae75f5694cb3676feff44873695919704be92f0c54785a4ef95e1b750a94645.jpg')
        self.extractor = data.get('extractor', 'None')
        self.requester = requester

    def read(self):
        return self.original.read()

    def cleanup(self):
        self.original.cleanup()

    def is_opus(self):
        return self.original.is_opus()

    async def load_source(self):
        self.original = await discord.FFmpegOpusAudio.from_probe(self.source_url, **ffmpeg_options)

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False, requester: User = ""):
        loop = loop or asyncio.get_event_loop()
        # gonna change this later
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            list_of_source = []
            for each_data in data['entries']:
                filename = each_data['url']
                source = cls(original=None,
                             data=each_data,
                             requester=requester)
                list_of_source.append(source)

            return list_of_source

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return [
            cls(original=None,
                data=data,
                requester=requester)
        ]

    @classmethod
    async def from_keywords(cls, keywords, *, loop=None, stream=False, requester: User = ""):
        loop = loop or asyncio.get_event_loop()
        # gonna change this later
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(f"ytsearch:{keywords}", download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return [
            cls(original=None,
                data=data,
                requester=requester)
        ]
