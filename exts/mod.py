import json
import discord
import mysql.connector as c
from discord.ext import commands

botconf = json.load(open('config.json'))

class Mod(commands.Cog):
    '''Moderation Commands'''

    def __init__(self,bot):
        self.bot = bot

    @commands.has_permissions(manage_messages=True, manage_roles=True)
    @commands.command(name='mute')
    async def mute(self, ctx, user:discord.Member,reason:str="Shut the up user"):
        '''Mute a user
        Mute a user to their mute jail cell\\nWho told them to misbehave, do this when you need to, but not abuse it.
        mute <user> [Reason]
        Manage messages, Manage roles'''
        await ctx.send('Connecting...',delete_after=4)
        async with ctx.channel.typing():
            0

    @mute.error
    async def moderr(self, ctx, error):
        await ctx.send(embed=discord.Embed(title='Command errored.'))

def setup(bot):
    bot.add_cog(Mod(bot))
