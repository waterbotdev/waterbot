import asyncio
import discord
import inspect
import json
import re
import subprocess

from .helpers.check import Checks
from discord.ext import commands

botConfig = json.load(open('config.json'))

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

            if len(str(result)) >= 2000:
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
        msg = await ctx.send(embed=discord.Embed(title='Updating...', description='Initializing...'))
        await asyncio.sleep(1)
        await msg.edit(embed=discord.Embed(title='Running `git fetch`...', description='Waiting for logs...', color=0xf7eb60))
        run = subprocess.run(['git','fetch'], stdout=subprocess.PIPE)
        await msg.edit(embed=discord.Embed(title='Running git fetch...',description=f'```{"No Logs."}```', color=0xf7eb60))
        await asyncio.sleep(3)
        await msg.edit(embed=discord.Embed(title='Running `git merge`...', description='Waiting for logs...', color=0xf7eb60))
        run = subprocess.run(['git', 'merge'], stdout=subprocess.PIPE)
        await msg.edit(embed=discord.Embed(title='Running `git merge`...', description=f'```py\n{run.stdout.decode()}```', color=0xf7eb60))
        await asyncio.sleep(3)
        await msg.edit(embed=discord.Embed(title='Running `starter.bat`...', description='Restarting...', color=0x31d90b))
        run = subprocess.run(['cmd','/K','starter.bat'])
        await msg.edit(embed=None,content='Restarting...')
        await ctx.bot.logout()


    @Checks.is_dev()
    @commands.command(name='announce')
    async def announce(self, ctx, size: str, title: str, *, details: str):
        '''Announce something
        Announce bot updates in the channel.
        announce <s|b> <title> <details>
        Developers only.'''
        if size == "small" or "minor" or "s":
            channel = ctx.bot.get_channel(botConfig['minornews'])
            color = 0xf5d442
        elif size == "big" or "major" or "b":
            channel = ctx.bot.get_channel(botConfig['majornews'])
            color = 0xf7401b
        else:
            return await ctx.send('Invalid size. \nIt have to be `s` or `b`, `minor` or `major`, `small` or `big`.')

        embed = discord.Embed(color=color, title=title, description=details, timestamp=ctx.message.created_at)
        embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await channel.send(embed=embed)
def setup(bot):
    bot.add_cog(Dev(bot))

# Testing 02
