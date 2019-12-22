import discord
import random
import requests
import json
import os
from discord.ext import commands
import base64
# tokenfile = open('token.txt','r')
# etokenb = tokenfile.read().encode()
# tokenb = base64.b64decode(etokenb)
# token = tokenb.decode()
token = os.environ["BOT_TOKEN"]
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
async def activity(ctx,*,text):
    """Sets the bots status (OWNER)"""
    #await ctx.send(content=" :ok_hand: What is the message you want in status")
    #message = await client.wait_for('message')
    #game = discord.Game(message.content)
    game = discord.Game(text)
    await bot.change_presence(status=discord.Status.online, activity=game)
    await ctx.send(':ok_hand: Done.')
@activity.error
async def activityError(ctx,error):
    await ctx.send("Command errored.\n{}".format(error))

@bot.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
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
    embed = discord.Embed(title='8 Ball Response', colour=0x000000,description=f"**Question**: {question}\n**Answer**: {random.choice(responses)} ")
    await ctx.send(embed=embed)

@bot.command()
async def help(ctx):
    embed = discord.Embed(colour=discord.Colour(0xd1e9fd), url="https://discordapp.com/")
    embed.set_author(name="waterbot - help", icon_url="https://cdn.discordapp.com/avatars/655262203309719552/ca12b1a43ea265c81535b83fb4d6fb21.png?size=128")
    embed.set_footer(text=f"Executed by {ctx.message.author}", icon_url=ctx.author.avatar_url)
    # help = {
    #     "Moderation":{
    #             ".mute":{
    #
    #             }
    #     }
    # }
    embed.add_field(name="Moderation", value=".mute, add whatever you want")
    embed.add_field(name="Utility", value=".activity, add whatever you want")
    embed.add_field(name="Fun", value=".8ball, add whatever you want")
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
async def invite(ctx):
    embed=discord.Embed(title="Invite Waterbot", url="https://cdn.discordapp.com/avatars/655262203309719552/ca12b1a43ea265c81535b83fb4d6fb21.png?size=128", description="use this link to add waterbot to your server!", color=0x8cff8f)
    embed.set_author(name="waterbot", url="https://cdn.discordapp.com/avatars/655262203309719552/ca12b1a43ea265c81535b83fb4d6fb21.png?size=128")
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/655262203309719552/ca12b1a43ea265c81535b83fb4d6fb21.png?size=128")
    embed.add_field(name="https://discordapp.com/api/oauth2/authorize?client_id=655262203309719552&permissions=8&scope=bot", value="waterbot", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def say(ctx, *, text):
    await ctx.send(text)

@bot.command()
async def userinfo(ctx,member:discord.Member=None):
    '''Get member info
    '''
    if member == None:
        member = ctx.author
    # Find user roles.
    roles = [role for role in member.roles]
    #roles = roles.remove(roles[0])
    #roles.remove(0)
    embed = discord.Embed(color=member.color, timestamp=ctx.message.created_at)
    embed.set_author(name=f"User Information - **{member}**")
    embed.set_thumbnail(url=member.avatar_url)
    embed.add_field(name="User ID:", value=member.id)
    embed.add_field(name="Created at:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
    embed.add_field(name="Joined at:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
    embed.add_field(name=f"Roles({len(roles)})", value=" ".join([role.mention for role in roles]))
    embed.add_field(name="Top Role:", value=[role.mention for role in [role for role in author.roles]][len([role.mention for role in [role for role in author.roles]])-1])
    embed.add_field(name="Is Bot?",  value=member.bot)

    await ctx.send(embed=embed)

@bot.command(name='ping')
async def ping(ctx):
    '''Get the ping of the bot to discord.
    Also used to check if bot is online.
    '''
    botping = ctx.bot.latency*1000
    if botping < 100:
        color = 0x55aa55
    elif botping < 500:
        color = 0xffff55
    else:
        color = 0xff5555
    await ctx.send(embed=discord.Embed(description=f"Bot ping: {botping}",colour=color))
bot.run(token)
