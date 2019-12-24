import discord
import random
from discord.ext import commands

class Fun(commands.Cog):
    '''Fun commands Category
    '''
    def __init__(self,bot):
        self.bot = bot

    # Start of commands
    @commands.command()
    async def fuck(self,ctx):
        '''Screw Kenny he's a dumbass
        - Kenny
        '''
        await ctx.send('shit')

    @commands.command()
    async def e(self,ctx):
        '''Something
        '''
        await ctx.send('e')

    @commands.command()
    async def fatfuck(self,ctx):
        '''Surprise.
        '''
        await ctx.send(embed=discord.Embed().set_image(url='https://cdn.discordapp.com/attachments/452733553122476062/655291803087667201/image0.png'))

    @commands.command(aliases=['8ball'])
    async def _8ball(self,ctx, *, question):
        '''Ask 8ball a question. You'll get a good answer.
        '''
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
    @_8ball.error
    async def _8ballerr(self,ctx,error):
        await ctx.send(f"Command errored.\n{error}")

    @commands.command()
    async def bunj(self,ctx):
        '''BUNJ BUNJ BUNJ BUNJ BUNJ
        '''
        embed=discord.Embed(title="bunj", url="https://cdn.discordapp.com/attachments/583070530706604034/655630309290934273/Snapchat-446272952.jpg", description="bunj", color=0x8cff8f)
        embed.set_author(name="bunj", url="https://cdn.discordapp.com/attachments/583070530706604034/655630309290934273/Snapchat-446272952.jpg", icon_url="https://cdn.discordapp.com/attachments/583070530706604034/655630309290934273/Snapchat-446272952.jpg")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/583070530706604034/655630309290934273/Snapchat-446272952.jpg")
        embed.add_field(name="bunj", value="bunj", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def pets(self,ctx,pet="random"):
        '''Get a pet image
        '''
        async with ctx.channel.typing():
            if pet == 'random':
                pet = random.choice(['dog','cat'])
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
    async def troll(self,ctx):
        '''Troll a user
        '''
        await ctx.send(embed=discord.Embed(title="Get trolled loser").set_image(url='https://cdn.discordapp.com/attachments/583070530706604034/655643417992495134/maxresdefault.jpg'))

def setup(bot):
    bot.add_cog(Fun(bot))
