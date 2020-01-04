import discord
import inspect
from discord.ext import commands


def is_dev():
    developers = [
        513603936033177620,
        513603936033177620,
        397029587965575170,
        397273885701177347
    ]
    async def predicate(ctx):
        return ctx.author.id in developers
    return commands.check(predicate)
class Dev(commands.Cog):
    '''Developer commands
    '''
    def __init__(self,bot):
        self.bot = bot
        
    @commands.command(name='die',aliases=['disconnect'])
    @is_dev()
    async def die(self,ctx):
        '''Kills the bot
        '''
        await ctx.send('Disconnecting...')
        await ctx.bot.logout()

    @is_dev()
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