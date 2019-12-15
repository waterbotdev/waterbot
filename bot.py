import discord
import random 
import requests
import json
from discord.ext import commands
import base64
tokenfile = open('token.txt','r')
etokenb = tokenfile.read().encode()
tokenb = base64.b64decode(etokenb)
token = tokenb.decode()
bot = commands.Bot(command_prefix='.')

bot.remove_command('help')


@bot.event
async def on_ready():
    print(f'Logged in as: {bot.user.name}')
    print(f'With ID: {bot.user.id}')


@bot.command()
async def fuck(ctx):
    await ctx.send('shit')


@bot.command()
async def e(ctx):
    await ctx.send('e')



@bot.command()
async def fatfuck(ctx):
    await ctx.send('https://cdn.discordapp.com/attachments/452733553122476062/655291803087667201/image0.png')


@bot.command(pass_context=True)
async def boostinfo(ctx):
    embed = discord.Embed(name="{}'s info".format(ctx.message.guild.name), color=0xd399f0)
    embed.set_author(name=f"Nitro Boosting Status for: {ctx.message.guild.name}")
    embed.add_field(name="Boost Amount", value=ctx.message.guild.premium_subscription_count)
    embed.add_field(name="Boost / Server Level", value=ctx.message.guild.premium_tier)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/571045753091522607/618829850656112650/Excalibur.png")
    embed.set_footer(text=f"Requested By: {ctx.message.author}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)


@bot.command()
@commands.is_owner()
async def activity(ctx) :
    '''Changes the status of the bot
    Bot Owner Only.
    '''
    await ctx.send(":ok_hand:")


@bot.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = ['It is certain.',
                'It is decidedly so.',
                'Without a doubt.',
                'Yes - definitely.',
                'You may rely on it.',
                'As I see it, yes.',
                'Most likely.',
                'Outlook good.',
                'Yes.',
                'Signs point to yes.',
                'Reply hazy, _try again.',
                'Oh! i forgot. It is tea time, _try another time!',
                'Ask again later, I am too busy.',
                'Better _not tell you now.',
                'Cannot predict now.',
                'Concentrate _and ask again.',
                'Don\'t count on it.'
                'My reply _is no.',
                'My sources say no.',
                'Outlook not so good',
                'Very doubtful.']
    embed = discord.Embed(title='8 Ball Response', colour=0x000000,description=f"**Question**: {question}\n**Answer**: {random.choice(responses)} ")
    await ctx.send(embed=embed)

   
@bot.command()
async def pet(ctx,pet="random"):
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


@bot.command()
async def bunj(ctx):     
    embed=discord.Embed(title="bunj", url="https://cdn.discordapp.com/attachments/583070530706604034/655630309290934273/Snapchat-446272952.jpg", description="bunj", color=0x8cff8f)
    embed.set_author(name="bunj", url="https://cdn.discordapp.com/attachments/583070530706604034/655630309290934273/Snapchat-446272952.jpg", icon_url="https://cdn.discordapp.com/attachments/583070530706604034/655630309290934273/Snapchat-446272952.jpg")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/583070530706604034/655630309290934273/Snapchat-446272952.jpg")
    embed.add_field(name="bunj", value="bunj", inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def troll(ctx):
    await ctx.send('get trolled loser https://cdn.discordapp.com/attachments/583070530706604034/655643417992495134/maxresdefault.jpg')


@bot.command()
async def help(ctx):

    embed = discord.Embed(colour=discord.Colour(0xd1e9fd), url="https://discordapp.com/%22)

    embed.set_author(name="waterbot - help", icon_url="https://cdn.discordapp.com/avatars/655262203309719552/ca12b1a43ea265c81535b83fb4d6fb21.png?size=1024%22)
    embed.set_footer(text=f"Executed by {ctx.message.author}", icon_url="ctx.author.avatar_url")

    embed.add_field(name="Moderation", value=".mute, add whatever you want")
    embed.add_field(name="Utility", value=".activity, add whatever you want")
    embed.add_field(name="Fun", value=".8ball, add whatever you want")

    await ctx.send(embed=embed)


bot.run(token)
