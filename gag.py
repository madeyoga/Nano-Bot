from nineapi.nineapi.client import  Client, APIException
import os
import sys
import random

import discord
from discord.ext import commands
from discord.ext.commands import Bot


class GagState:
    def __init__(self, bot):
        self.bot = bot
        self.current_group_id = -1
        self.current_post_list = []

class NineGag:
    def __init__(self, bot):
        self.bot = bot
        self.gag_states = {}

    def get_gag_client(self):
        client = Client()
        client.log_in(str( os.environ.get('GAG_USERNAME')), str(os.environ.get('GAG_PASSWORD')) )
        return client
    
    def get_gag_state(self, server):
        state = self.gag_states.get(server.id)
        if state is None:
            state = GagState(self.bot)
            self.gag_states[server.id] = state
        return state

    def get_embedded_gag(self, group_id, state):
        
        client = self.get_gag_client()
        
        if not state.current_group_id == group_id:
            state.current_group = group_id
            state.current_post_list.clear()
            posts = client.get_posts(group=group_id, count=50, type_='hot', entry_types=['photo'])
            for post in posts:
                state.current_post_list.append(post)
            rand_numb = random.randint(0, len(posts) - 1)
            embed = discord.Embed(title=posts[rand_numb].title, description="powered by nineapi", color=0x000000)
            embed.set_image(url=posts[rand_numb].get_media_url())
            return embed
        else:
            rand_numb = random.randint(0, len(state.current_post_list) - 1)
            embed = discord.Embed(title=state.current_post_list[rand_numb].title, description="powered by nineapi", color=0x000000)
            embed.set_image(url=state.current_post_list[rand_numb].get_media_url())
            return embed
    
    @commands.command(pass_context=True)
    async def anime(self, ctx):
        state = self.get_gag_state(ctx.message.server)
        embed = self.get_embedded_gag(32, state)    
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def wtf(self, ctx):
        state = self.get_gag_state(ctx.message.server)
        embed = self.get_embedded_gag(4, state)
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def savage(self, ctx):
        state = self.get_gag_state(ctx.message.server)
        embed = self.get_embedded_gag(45, state)
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def kpop(self, ctx):
        state = self.get_gag_state(ctx.message.server)
        embed = self.get_embedded_gag(34, state)
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def cosplay(self, ctx):
        state = self.get_gag_state(ctx.message.server)
        embed = self.get_embedded_gag(11, state)
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def comic(self, ctx):
        state = self.get_gag_state(ctx.message.server)
        embed = self.get_embedded_gag(17, state)
        await self.bot.say(embed=embed)
    
def setup(bot):
    bot.add_cog(NineGag(bot))
    print('9Gag is loaded')
