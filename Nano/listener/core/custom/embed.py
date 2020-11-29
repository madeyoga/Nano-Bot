import discord
from discord import Embed


class CustomEmbed(Embed):

    def __init__(self):
        super().__init__(color=discord.Color(value=11735575).orange())
