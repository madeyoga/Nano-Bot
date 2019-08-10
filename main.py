import discord
from listener.core.client import NanoClient as Client
from listener.core import config

startup_extensions = [
    'listener.general_commands',
    'listener.image_commands',
    'listener.music_commands',
    #'listener.gacha_commands'
]

client = Client(command_prefix='n>')
client.remove_command('help')

# Discord Bot List updates.
dbl_token = os.environ['DBL_TOKEN']
BASE_URL = "https://discordbots.org/api/bots/458298539517411328/stats"
headers = {"Authorization": dbl_token}

async def update_status_on_dbl():
    payload = {"server_count" : len(client.guilds)}
    async with aiohttp.ClientSession() as session:
        await session.post(BASE_URL, data=payload, headers=headers)

@client.event
async def on_ready():
    status_message = discord.Game("n>help")
    await client.change_presence(status=discord.Status.online, activity=status_message)
    await update_status_on_dbl()

@client.event
async def on_guild_join():
    """Updates DBL when client joins a guild"""
    await update_status_on_dbl()

@client.event
async def on_guild_leave():
    """Updates DBL when client leaves a guild"""
    await update_status_on_dbl()

if __name__ == '__main__':
    for extension in startup_extensions:
#         try:
        client.load_extension(extension)
#         except Exception as e:
#             exc = '{}: {}'.format(type(e).__name__, e)
#             print('Failed to load extension {}\n{}'.format(extension, exc))

client.run(config.BOT_TOKEN)
