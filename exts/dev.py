import discord
import inspect
import json
import re

from .helpers.check import Checks
from discord.ext import commands

class Dev(commands.Cog):
    '''Developer commands'''
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name='die',aliases=['disconnect'])
    @Checks.is_dev()
    async def die(self,ctx):
        '''Kills the bot
        Kills the bot
        die
        Developers only'''
        await ctx.send('Disconnecting...')
        await ctx.bot.logout()

    @commands.command(aliases=['eval'])
    @Checks.is_dev()
    async def evaluate(self, ctx, *, code:str):
        '''Run some code.
        Runs a code snippet
        evaluate|eval <code>
        Developers only'''
        async with ctx.channel.typing():
            result = None
            env = {'ctx': ctx,}
            env.update(globals())
            try:
                result = eval(code, env)
                if inspect.isawaitable(result):
                    result = await result
                await ctx.message.add_reaction("✔️")
            except Exception as e:
                result = type(e).__name__ + ': ' + str(e)
                await ctx.message.add_reaction("✖️")
        try:
            await ctx.channel.send('```py\n{}```'.format(result))
        except discord.errors.Forbidden:
            pass


def setup(bot):
    bot.add_cog(Dev(bot))