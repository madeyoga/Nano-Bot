from abc import ABC

import discord
import youtube_dl
import asyncio

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
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn -nostats -loglevel 0'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class AudioTrack(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=1.0):
        super().__init__(source, volume=volume)

        self.title = data.get('title')
        self.url = data.get('webpage_url')
        self.duration = parse_duration(int(data.get('duration')))
        self.thumbnail = data.get('thumbnail')
        self.extractor = data.get('extractor')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        # gonna change this later
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            list_of_source = []
            for each_data in data['entries']:
                filename = each_data['url']
                source = cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=each_data)
                list_of_source.append(source)

            return list_of_source

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return [cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)]

    @classmethod
    async def from_keywords(cls, keywords, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        # gonna change this later
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(f"ytsearch:{keywords}", download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return [cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)]

