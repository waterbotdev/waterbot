import discord
import random
import requests
import json
from discord.ext import commands


class Fun(commands.Cog):
    '''Fun commands Category
    '''

    def __init__(self, bot):
        self.bot = bot

    # Start of commands
    @commands.command()
    async def fuck(self, ctx):
        '''Fuck
        For when you fucked up your life.
        fuck
        Send messages'''
        await ctx.send('shit')

    @commands.command()
    async def e(self, ctx):
        '''Something
        Mark is something wrong there? Why is your face square?
        e
        Send messages'''
        await ctx.send('e')

    @commands.command()
    async def fatfuck(self, ctx):
        '''Surprise.
        pika pika fuck
        fatfuck
        Send messages'''
        await ctx.send(embed=discord.Embed().set_image(
            url='https://cdn.discordapp.com/attachments/452733553122476062/655291803087667201/image0.png'))

    @commands.command(aliases=['8ball'])
    async def _8ball(self, ctx, *, question):
        '''Le Magiko 8 bowling ball
        Ask 8ball a question. You'll get a good answer. Or not. :eyes:
        8ball <question>
        Send messages'''
        responses = ['It is certain.',
                     'It is decidedly so.',
                     'Without a doubt.',
                     'Yes, definitely.',
                     'You may rely on it.',
                     'As I see it, yes.',
                     'Most likely.',
                     'Outlook good.',
                     'Yes.',
                     'Signs point to yes.',
                     'Reply hazy, _try again._',
                     'Oh! i forgot. It is tea time, _try another time!_',
                     'Ask again later, I am too busy.',
                     'Better _not tell you now._',
                     'Cannot predict now.',
                     'Concentrate _and ask again_.',
                     'Don\'t count on it.'
                     'My reply _is no_.',
                     'My sources say no.',
                     'Outlook not so good',
                     'Very doubtful.']
        embed = discord.Embed(title='8 Ball Response',
                              colour=0x000000,
                              description=f"**Question**: {question}\n**Answer**: {random.choice(responses)} ")
        await ctx.send(embed=embed)

    # @_8ball.error
    # async def _8ballerr(self, ctx, error):
    #     await ctx.send(f"Command errored.\n{error}")

    @commands.command()
    async def bean(self, ctx, user: discord.User, *, reason: str = "no Reason"):
        '''Ban a user
        Sometimes you gotta humiliate your friends and feed them beans.
        bean [user] <reason>
        Send messages'''
        await ctx.send(f"{user} `({user.id})` has been beaned. Reason `{reason}`")

    # @bean.error
    # async def beanerror(self, ctx):
    #     await ctx.send(f':kite: Invalid argument.\nCommand Usage: `.bean <user> [reason>]`')

    @commands.command()
    async def fight(self, ctx, user: discord.User, *, reason: str = "no Reason"):
        '''Fights a user
        Beat the shit out of someone, possibly your friend.
        fight [user] <reason>
        Send messages'''
        await ctx.send(f"<:catfight:668814428111896586> {ctx.author.name} is killing {user.mention} for `{reason}`.")

    # @fight.error
    # async def fighterror(self, ctx):
    #     await ctx.send(f':kite: Invalid argument.\nCommand Usage: `.fight <user> [reason>]`')

    @commands.command()
    async def spray(self, ctx, user: discord.User, *, reason: str = "no Reason"):
        '''Spray a user
        s p  r   a    y
        spray [user] <reason>
        Send messages'''
        await ctx.send(
            f"<a:sprayspray:668814655082463252> {ctx.author.name} is spraying on you, {user.mention} for `{reason}`!")

    # @spray.error
    # async def sprayerror(self, ctx):
    #     await ctx.send(f':kite: Invalid argument.\nCommand Usage: `.spray <user> [reason>]')

    @commands.command()
    async def choose(self, ctx, *, choices: str):
        '''Choose something.
        Let the bot decide something for you.
        choose [objct1], [object2], ...
        Send messages'''
        await ctx.send(f'{(random.choice(choices.split(",")))}, I choose you!')

    @commands.command()
    async def reverse(self, ctx, *, text: str):
        '''Let the bot reverse your text.
        reverse any text you'd like 
        reverse [text]
        Send messages'''
        t_rev = text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
        await ctx.send(f"{t_rev}")

    @commands.command()
    async def rate(self, ctx, *, thing: commands.clean_content):
        '''Let the bot rate someone
        Rate your crush's status with you 😳
        rate 
        Send messages'''
        num = random.randint(100, 10000) / 100
        await ctx.send(f"I'd rate `{thing}` a **{num} / 100**")

    @commands.command()
    async def respect(self, ctx, *, text: commands.clean_content = None):
        '''f in chat
        If you don't know this meme, jump in a microwave.
        f
        Send messages'''
        hearts = [':red_heart:', ':yellow_heart:', ':green_heart:', ':blue_heart:', ':purple_heart:']
        reason = f"for **{text}** " if text else ""
        await ctx.send(f"**{ctx.author.name}** has paid their respect {reason}{random.choice(hearts)}")

    @commands.command()
    async def pets(self, ctx, pet="random"):
        '''Get a pet image
        Get a pet image if you don't specify which pet. \\nCurrently supports [cat,dog]\\nWill output a random pet picture if not specified.
        pet [animal]
        Send messages'''
        async with ctx.channel.typing():
            if pet == 'random':
                pet = random.choice(['dog', 'cat'])
                if pet == 'dog' or 'cat':
                    rawres = requests.get(f'https://api.the{pet}api.com/v1/images/search')
                    url = json.loads(rawres.text)[0]['url']
                    embed = discord.Embed(title=f"Random {pet} image")
                    embed.set_image(url=url)
                    embed.set_footer(text=f"Powered by the{pet}api.com")
                    await ctx.send(embed=embed)
                    return
                else:
                    await ctx.send('Invalid pet specified.')

    @commands.command()
    async def coinflip(self, ctx):
        '''Flip a coin
        Flip that coin
        coinflip 
        None'''
        choices = ["Heads!", "Tails!"]
        rancoin = random.choice(choices)
        await ctx.send(rancoin)
        
def setup(bot):
    bot.add_cog(Fun(bot))
