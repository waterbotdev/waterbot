import asyncio
import discord
import inspect
import json
import re
import subprocess

from .helpers.check import Checks
from discord.ext import commands


class Dev(commands.Cog):
    '''Developer commands'''

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='die', aliases=['disconnect'])
    @Checks.is_dev()
    async def die(self, ctx):
        '''Kills the bot
        Kills the bot
        die
        Developers only'''
        await ctx.send(
            f'<:angrysponge:668767678273683474> You\'ve made a big fault, {ctx.author.mention}. The bell of awakening is coming soon for you..')
        await ctx.bot.logout()

    @commands.command(aliases=['eval'])
    @Checks.is_dev()
    async def evaluate(self, ctx, *, code: str):
        '''Run some code.
        Runs a code snippet
        evaluate|eval <code>
        Developers only'''
        async with ctx.channel.typing():
            result = None
            env = {'ctx': ctx}
            env.update(globals())
            try:
                result = eval(code, env)
                if inspect.isawaitable(result):
                    result = await result
                await ctx.message.add_reaction("✔")
            except Exception as e:
                result = type(e).__name__ + ': ' + str(e)
                await ctx.message.add_reaction("✖")

            if len(result) >= 2000:
                await ctx.send('Result length is larger than 2000! Sending the first 2000 characters.')
                return await ctx.send(f'```py\n{result[0:2000]}```')
            try:
                await ctx.channel.send('```py\n{}```'.format(result))
            except Exception as e:
                await ctx.send(e)

    @Checks.is_dev()
    @commands.command(name='gitpull', aliases=['gpull', 'pull'])
    async def gitpull(self, ctx):
        '''Update local repo
        Updates local code repo from github.
        [gitpull|gpull|pull]
        Developers only'''
        embed = discord.Embed(title='testing', description='0%')
        msg = await ctx.send(embed)
        await asyncio.sleep(2)
        await msg.edit(embed=discord.Embed(title='testing', description='10%', color=0xfcdb03))
        await asyncio.sleep(2)
        await msg.edit(embed=discord.Embed(title='testing', description='20%', color=0xfcdb03))
        await asyncio.sleep(2)
        await msg.edit(embed=discord.Embed(title='testing', description='30%', color=0xfcdb03))
        await asyncio.sleep(2)
        await msg.edit(embed=discord.Embed(title='testing', description='40%', color=0xfcdb03))
        await asyncio.sleep(2)
        await msg.edit(embed=discord.Embed(title='testing', description='50%', color=0xfcdb03))
        await asyncio.sleep(2)
        await msg.edit(embed=discord.Embed(title='testing', description='100%', color=0x31d90b))


def setup(bot):
    bot.add_cog(Dev(bot))
