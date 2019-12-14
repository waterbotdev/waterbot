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
@bot.is_owner()
async def activity(ctx):

    await ctx.send(content=" :ok_hand: What is the message you want in status")
    message = await bot.wait_for('message')
    game = discord.Game(message.content)
    await bot.change_presence(status=discord.Status.online, activity=game)


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
async def cat(ctx):
    async with ctx.channel.typing():                            
      rawres = requests.get('https://api.thecatapi.com/v1/images/search')
      parres = json.loads(rawres.text)
      url = parres[0]["url"]
      embed = discord.Embed(title="Random Cat Image")
      embed.set_image(url=url)
      embed.set_footer(text="Powered by thecatapi.com!")                                                              
    await ctx.send(embed=embed)


@bot.command()
async def dog(ctx):
    async with ctx.channel.typing():                            
      rawres = requests.get('https://api.thedogapi.com/v1/images/search')
      parres = json.loads(rawres.text)
      url = parres[0]["url"]
      embed = discord.Embed(title="Random Dog Image")
      embed.set_image(url=url)
      embed.set_footer(text="Powered by thedogapi.com!")                                                              
    await ctx.send(embed=embed)

@bot.command()
async def help(ctx):
embed = discord.Embed(colour=discord.Colour(0xfff0d2), url="https://discordapp.com", timestamp=datetime.datetime.utcfromtimestamp(1576318214))

embed.set_author(name="waterbot - help", icon_url="https://cdn.discordapp.com/avatars/655262203309719552/ca12b1a43ea265c81535b83fb4d6fb21.png?size=1024")
embed.set_footer(text=f"Executed by {ctx.message.author}", icon_url="ctx.author.avatar_url")

embed.add_field(name="Moderation", value="`.mute`, `add whatever you want`")
embed.add_field(name="Utility", value="`.activity`, `add whatever you want`")
embed.add_field(name="Fun", value="`.8ball`, `add whatever you want`")

await ctx.send(embed=embed)


bot.run(token)