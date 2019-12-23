import discord
import inspect
from discord.ext import commands
from .helpers.check import checks

class Dev(commands.Cog):
    '''Developer commands
    '''
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name='die',aliases=['disconnect'])
    @checks.is_dev()
    async def die(self,ctx):
        '''Kills the bot
        '''
        await ctx.send('Disconnecting...')
        await ctx.bot.logout()

    @commands.command(aliases=['eval'])
    async def evaluate(self, ctx, *, code:str):
        '''Run some code.
        '''
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
