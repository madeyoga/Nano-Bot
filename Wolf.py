import discord
from discord.ext import commands
from discord.ext.commands import Bot
import io
import asyncio
import os
import random
import re
from pathlib import Path

class Player:
    def __init__(self, message, role=None):
        self.player = message.author
        self.channel = message.channel        
        self.role = role

class GameState:
    def __init__(self, bot):
        self.bot = bot
        self.players = []
        self.registry_open = False
        self.playing = False
        self.pause = True
        self.day = 0
        self.the_day = True
        self.active_messages = []
        self.responded_messsage = 0
        
        # Random player's role
        self.random_numb_list = []
        while len(self.random_numb_list) < 5:
            random_numb = random.randint(1, 5)
            if not random_numb in self.random_numb_list:
                self.random_numb_list.append(random_numb)

class Wolf:
    def __init__(self, bot):
        self.bot = bot
        self.game_states = {}
        
    def get_game_state(self, server):
        state = self.game_states.get(server.id)
        if state is None:
            state = GameState(self.bot)
            self.game_states[server.id] = state
        return state

    @commands.command(pass_context=True)
    async def wolf(self, ctx):
        state = self.get_game_state(ctx.message.server)
        if not state.registry_open:
            state.registry_open = True
            embed = discord.Embed(title=":tada: Starting Wolf Game!! :tada:", description=" .ready to participate",  color=0x0000ff)
            await self.bot.say(embed=embed)
        else:
            embed = discord.Embed(title="The Game is already started",  color=0x0000ff)
            # Handle BUGS HERE !
            await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def wolfstop(self, ctx):
        state = self.get_game_state(ctx.message.server)
        if state.playing:
            state.playing=False
            embed = discord.Embed(title="The game has ended~", description=" bye~",  color=0x0000ff)
            await self.bot.say(embed=embed)
            del self.game_states[ctx.message.server.id]
        else:
            embed = discord.Embed(title="Not playing anything",  color=0x0000ff)
            await self.bot.say(embed=embed)
    
    @commands.command(pass_context=True)
    async def ready(self, ctx):
        server = ctx.message.server
        state = self.get_game_state(server)
        if state.registry_open:
            role = ""
            if state.random_numb_list[0] == 1:
                role = "Wolf"
            elif state.random_numb_list[0] == 2:
                role = "Guardian"
            elif state.random_numb_list[0] == 3:
                role = "Hunter"
            else:
                role = "Villager"
            state.players.append(Player(ctx.message, role))
            state.random_numb_list.pop(0)
            desc = "{}/5".format(str(len(state.players)))
            embed = discord.Embed(title="{} is joining the Game! :tada:".format(ctx.message.author.name), description=desc, color=0x0000ff)
            await self.bot.say(embed=embed)
            if len(state.players) == 5:
                state.registry_open = False
                state.playing = True
                embed = discord.Embed(title=":tada: The game is now ready, i will DM you guys the role now~", color=0x0000ff)
                await self.bot.say(embed=embed)
                for i in range(0, 5):
                    msg = "your role is ... {}\nSSSHH! Don't tell anyone about it! the truth!\n"
                    if state.players[i].role == "Wolf":
                        msg+="Your task is to kill all the villagers! but you also can kill others than villager, like Guardian, Hunter, etc\n"
                        msg+="as long as it is not Guarded by the Guardian\n"
                        msg+="I will dm you every turn~"
                    elif state.players[i].role == "Guardian":
                        msg+="Your task is to guard your friend from wolfs every night.\n"
                        msg+="you should choose one of your friend to be guarded~\n\nOH! and you cannot guard your self\n"
                        msg+="lmao"
                    elif state.players[i].role == "Hunter":
                        msg+="Your task is to kill the wolf, to save the villagers from wolfs.\n"
                        msg+="i will DM you every night~ list of people you want to pew pew!!"
                    else: # villager
                        msg+="Hello, You're just a normal villagers!\n"
                        msg+="you should go and tell your friend to protect you!"
                        
                    await self.bot.send_message(state.players[i].player, msg.format(state.players[i].role))

    @commands.command(pass_context=True)
    async def resume_wolf(self, ctx):
        server = ctx.message.server
        state = self.get_game_state(server)
        if state.the_day:
            if state.day == 0:
                news="There is 2 Wolves, 1 Guardian, 1 Hunter, 2 Villagers\n"
                news+="discuss with your friend, about how to survive and win against the wolfs\n"
                news+="remember!! 2 of your friends are the WOLVES here, so, keep quite about your role if you didnt want to get targeted by the wolves"
                embed = discord.Embed(title="The DAY! Day {}'s NEWS!".format(state.day), description=news, color=0x0000ff)
                embed.add_field(name="to resume", value="type .next_day to proceed to THE NIGHT!")
                await self.bot.send_message(state.players[0].channel, embed=embed)
            else:
                embed = discord.Embed(title="The DAY! Day {}".format(state.day), description="Werewolf game", color=0x0000ff)
                await self.bot.send_message(state.players[0].channel, embed=embed)
            state.the_day = False
        else: # the night
            embed = discord.Embed(title="The Night~ Day {}".format(state.day), description="please wait while the roles are taking action", color=0x0000ff)
            await self.bot.send_message(state.players[0].channel, embed=embed)
            for i in range(0, 5):
                title = ""
                desc = ""
                val = ""
                if state.players[i].role == "Wolf":
                    title = "Wolf"
                    desc = "choose 1 friend to kill"
                    val = "eat {}"
                elif state.players[i].role == "Guardian":
                    title = "Guardian"
                    desc = "choose 1 friend to Protect"
                    val = "protect {}"
                elif state.players[i].role == "Hunter":
                    title = "Hunter"
                    desc = "choose 1 friend that you taught he/she was the wolf"
                    val = "Pew Pew {}"
                else: # villagers
                    continue

                embed = discord.Embed(title=title, description=desc, color=0x0000ff)
                count = 1
                for player in state.players:
                    embed.add_field(name=str(count) + ". {}".format(player.player.name), value=val.format(player.player.name))
                    count+=1

                message = await self.bot.send_message(state.players[i].player, title, embed=embed)
                state.active_messages.append(message.id)
                
            # end of else, update, to the next day and the_day = true
            state.day += 1
            state.the_day = True
    
def setup(bot):
    bot.add_cog(Wolf(bot))
    print('Wolf is loaded')
