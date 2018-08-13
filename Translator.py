from googletrans import Translator

import discord
from discord.ext import commands
from discord.ext.commands import Bot

class SourceState:
    def __init__(self, bot):
        self.bot = bot
        self.source_id = ""
        self.dest_id = "en"
        self.translator = Translator()
        self.active_message = None
        self.is_dest=True

class Translators: 
    def __init__(self, bot):
        self.bot = bot
        self.source_states = {}

    async def on_reaction_add(self, reaction, user):
        state = self.get_source_state(reaction.message.server)
        if state.active_message and state.active_message.id == reaction.message.id and not reaction.emoji == "🎵":
            emoji = reaction.emoji
            index = "en"
            if emoji == "2⃣":
                index = "ja"
            elif emoji == "3⃣":
                index = "ko"
            if state.is_dest:
                state.dest_id=index
            else:
                state.source_id=index
            state.active_message = None
            await self.bot.delete_message(reaction.message)


    def get_source_state(self, server):
        state = self.source_states.get(server.id)
        if state is None:
            state = SourceState(self.bot)
            self.source_states[server.id] = state
        return state

    def get_embedded_options(self, to=None):
        embed = discord.Embed(color=0x000088)
        embed.set_author(name="options")
        if to:
            x = "to"
        else:
            x = "from"
        embed.add_field(name="1. en", value="translate " + x + " English", inline=False)
        embed.add_field(name="2. ja", value="translate " + x + " Japanese", inline=False)
        embed.add_field(name="3. ko", value="translate " + x + " Korean", inline=False)
        return embed

    @commands.command(pass_context=True)
    async def translate_to(self, ctx):
        state = self.get_source_state(ctx.message.server)
        state.is_dest=True
        msg = await self.bot.say(embed=self.get_embedded_options(True))
        await self.bot.add_reaction(msg, emoji="1⃣")
        await self.bot.add_reaction(msg, emoji="2⃣")
        await self.bot.add_reaction(msg, emoji="3⃣")
        await self.bot.add_reaction(msg, emoji="🎵")
        state.active_message = msg

    @commands.command(pass_context=True)
    async def translate_from(self, ctx):
        state = self.get_source_state(ctx.message.server)
        state.is_dest=False
        msg = await self.bot.say(embed=self.get_embedded_options(False))
        await self.bot.add_reaction(msg, emoji="1⃣")
        await self.bot.add_reaction(msg, emoji="2⃣")
        await self.bot.add_reaction(msg, emoji="3⃣")
        
        await self.bot.add_reaction(msg, emoji="🎵")
        state.active_message = msg

    @commands.command(pass_context=True)
    async def translate(self, ctx, *args):
        state = self.get_source_state(ctx.message.server)
        words = ""
        for word in args:
            words+=word
            words+=" "
        if state.source_id != "":
            result = state.translator.translate(words, dest=state.dest_id, src=state.source_id).text
        else:
            result = state.translator.translate(words, dest=state.dest_id).text
        await self.bot.say(result) 

def setup(bot):
    bot.add_cog(Translators(bot))
    print("Translator is loaded")
