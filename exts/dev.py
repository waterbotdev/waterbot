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
        msg = await ctx.send(embed=discord.Embed(title='Updating...', description='Initalizing...'))
        await asyncio.sleep(1)
        await msg.edit(embed=discord.Embed(title='Running `git fetch`...', description='Waiting for logs...', color=0xf7eb60))
        run = subprocess.run(['git','fetch'], stdout=subprocess.PIPE)
        await msg.edit(embed=discord.Embed(title='Running git fetch...',description=f'```{run.stdout.decode()}```', color=0xf7eb60))
        await asyncio.sleep(3)
        await msg.edit(embed=discord.Embed(title='Running `git merge`...', description='Waiting for logs...', color=0xf7eb60))
        run = subprocess.run(['git', 'merge'], stdout=subprocess.PIPE)
        await msg.edit(embed=discord.Embed(title='Running `git merge`...', description=f'```py\n{run.stdout.decode()}```', color=0xf7eb60))
        await asyncio.sleep(3)
        await msg.edit(embed=discord.Embed(title='Running `starter.bat`...', description='Restarting...', color=0x31d90b))
        run = subprocess.run(['start','cmd','starter.bat'])
        await msg.edit(embed=None,content='Restarting...')
        await ctx.bot.logout()


def setup(bot):
    bot.add_cog(Dev(bot))

# Testing 01
