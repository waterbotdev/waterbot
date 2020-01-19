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
        # await ctx.send('Connecting...',delete_after=4)
        async with ctx.channel.typing():
            embed = discord.Embed(title='Non',description='Not finished yet please stop using :pleading_face;')
        await ctx.send(embed=embed)

    @mute.error
    async def moderr(self, ctx, error):
        await ctx.send(embed=discord.Embed(title='Command errored.'))

    @commands.has_permissions(manage_messages=True)
    @commands.command(name='prune',aliases=['remove','clear'])
    async def prune(self, ctx, amount:int, members:commands.Greedy[discord.Member]=None):
        '''Clear messages
        Clear a number of messages, either globally or just from a user.
        [prune|remove|clear] <amount of messages> [User mention(s)]
        Manage Messages'''
        users = ''
        if members is not None:
            def check(m):
                for i in members:
                    if m.author == i:
                        return True
                    else:
                        pass
                return False
            try:
                ret = await ctx.channel.purge(limit=amount,check=check)
            except Exception as e:
                return await ctx.send(embed=discord.Embed(title='Command Errored.',description=e))
            for i in members:
                users += i.mention
        else:
            try:
                ret = await ctx.channel.purge(limit=amount)
            except Exception as e:
                return await ctx.send(embed=discord.Embed(title='Command Errored.',description=e))
        sornah = "s" if len(ret) > 1 else ""
        embed = discord.Embed(description=f'Deleted {len(ret)} message{sornah} {f"from {users}" if users != "" else ""}')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Mod(bot))
