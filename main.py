import discord
from listener.core.client import NanoClient as Client
from listener.core import config

startup_extensions = [
    'listener.general_commands',
    'listener.image_commands',
    'listener.music_commands',
    #'listener.gacha_commands'
]

client = Client(command_prefix='do.')
client.remove_command('help')

if __name__ == '__main__':
    for extension in startup_extensions:
        try:
            client.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

client.run(config.BOT_TOKEN)
