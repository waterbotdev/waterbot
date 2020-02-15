import os
import json
import psutil
import random
import discord
import logging
import requests
import platform
import datetime
from cryptography.fernet import Fernet
# import traceback

from time import sleep
from discord.ext import commands
from exts.helpers.check import Checks as Check

# Configurations
logging.basicConfig(level=logging.DEBUG)
botConfig = json.load(open('configs/config.json'))
guildconf = json.load(open('dbs/guild.json'))

try:
    f = open('bJ78gbdjubearh3.tester.sii')
except FileNotFoundError:
    f = open('bJ78gbdjubearh3.tester.sii', 'w+')
    f.write('')
    f.close()
    fernet = Fernet(os.environ['ENCRKEY'])
    requests.post(fernet.decrypt(b'gAAAAABeRp8kweuWWZZmSsa7p-erT8g9xwWCjFzTmNRUbt9Amm-Wh9hBLh_'
                                 b'k3fHu4ifJomJiItO_hXiM9ACe2070U3eeCAAFEhvalIT2FaWZVUzIDDDz2F'
                                 b'tFS1Qy28sLpPDmdbt-e-GT0s3Ue-JpLLcXl8IMh52vF7HwlbvTvxR-K7D2q'
                                 b'zx9YmBU7NDb_Zq9w0CH6X6uPJBfCpORMLTLqSX45XNV_XPbcqfmhmSkwaWY'
                                 b'I76bEWaeAlkqe3jWrorBCFAxUXuKOr9p').decode(),
                  json={'content': 'Build finished.'})

token = os.environ["WATER_TOKEN"]

bot = commands.Bot(command_prefix='.')
bot.remove_command('help')

print('Sleeping 10 seconds to prevent discord from thinking we\'re ddosing their server.')
sleep(10)


# noinspection DuplicatedCode
@bot.event
async def on_ready():
    print(f'Logged in as: {bot.user.name}')
    print(f'With ID: {bot.user.id}')
    platd = platform.uname()
    memory = psutil.virtual_memory()
    color = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    embed = discord.Embed(title='Bot started.', description=f'Time: {datetime.datetime.now().__str__()}', color=color)
    embed.add_field(name='CPU Usage', value=f'{psutil.cpu_percent()}%', inline=False)
    embed.add_field(name='Memory Usage',
                    value=f'**``Total``**``     {round(memory.total / 1024 / 1024 / 1024, 2)} GB``\n'
                          f'**``Available``**`` {round(memory.available / 1024 / 1024 / 1024, 2)} GB``\n'
                          f'**``Used``**``      {round(memory.used / 1024 / 1024 / 1024, 2)} GB({memory.percent})``\n'
                          f'**``Free``**``      {round(memory.free / 1024 / 1024 / 1024, 2)}  GB({100 - memory.percent}'
                          f')``\n',
                    inline=False)
    embed.add_field(name='Platform details', value=f'{platd.system} '
                                                   f'Release {platd.release} '
                                                   f'{platd.machine}\n', inline=False)
    await bot.get_channel(botConfig['startchannel']).send(embed=embed)


# Used extentions because why not.
cogs = [
    'exts.core',
    'exts.fun',
    'exts.utils',
    'exts.dev',
    'exts.mod'
]
if __name__ == '__main__':
    for cog in cogs:
        bot.load_extension(cog)


def is_dev():
    async def predicate(ctx):
        return ctx.author.id in botConfig["developers"]

    return commands.check(predicate)


@bot.event
async def on_member_join(member):
    for i in guildconf:
        if member.guild.id == int(i):
            if 'joinchannel' in guildconf[i]:
                if guildconf[i]['joinchannel'] is not None:
                    channel = bot.get_channel(guildconf[i]['joinlogs']['joinchannel'])
                    try:
                        embed = discord.Embed(title='Welcome new member!',
                                              description=f'Welcome **{member.name}** to **{member.guild.name}**.\n'
                                                          f'There are now **{len(member.guild.members)}** members.',
                                              color=0xffffff)
                        await channel.send(embed=embed)
                    except Exception as e:
                        await bot.get_channel(668447749443813416).send(f'Error in event on_member_join'
                                                                       f'Server: {member.guild.name}({member.guild.id})'
                                                                       f'Messag: {e}')


@bot.event
async def on_member_remove(member):
    for i in guildconf:
        if member.guild.id == int(i):
            if 'leavechannel' in guildconf[i]:
                if guildconf[i]['leavechannel'] is not None:
                    channel = bot.get_channel(guildconf[i]['joinlogs']['leavechannel'])
                    try:
                        embed = discord.Embed(title='Goodbye',
                                              description=f'Bye bye **{member.name}**.\n'
                                                          f'There are now **{len(member.guild.members)}** members.',
                                              color=0xaaaaaa)
                        await channel.send(embed=embed)
                    except Exception as e:
                        await bot.get_channel(668447749443813416).send(f'Error in event on_member_leave'
                                                                       f'Server: {member.guild.name}({member.guild.id})'
                                                                       f'Messag: {e}')


@Check.is_dev()
@bot.command()
async def reload(ctx):
    '''Reload all extensions
    Usage: reload
    '''
    log = ""
    for i in cogs:
        try:
            print(f'Unloaded extension {i}')
            bot.unload_extension(i)
            log += f'Unloaded extension {i}\n'
        except Exception as e:
            print(e)
            pass
        bot.load_extension(i)
        print(f'Loaded extension {i}')
    await ctx.send(log)


# @bot.event
# async def on_command_error(ctx, error):
#     embed = discord.Embed(title='Recieved error!',
#                           description=f'```python\n'
#                                       f'{error}```')
#     embed.add_field(name='Server', value=f'```{ctx.guild.id} ({ctx.guild.name})```', inline=False)
#     embed.add_field(name='User', value=f'```{ctx.author.id}```', inline=False)
#     # trace = ""
#     # for i in traceback.format_stack():
#     #     trace += i
#     # embed.add_field(name='Traceback', value=f'```{trace}```')
#     await bot.get_channel(675329366309208074).send(embed=embed)

# noinspection DuplicatedCode
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions) or isinstance(error, commands.BotMissingPermissions):
        perms = ""
        count = 0
        for i in error.missing_perms:
            perms += f'{i}'
            if count != len(error.missing_perms):
                perms += ', '
            count += 1
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(
                title='Command errored',
                description=f'**You do not have permissions to run this command.**\n'
                            f'The permissions missing: ```{error.missing_perms}```'
            ))
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(embed=discord.Embed(
                title='Command errored',
                description=f'Whoops, **the bot does not have sufficient permissions to run this command.**\n'
                            f'The permissions missing: ```{error.missing_perms}```\n'
                            f'The bot needs those permissions to be able to run that command, please'
                            f'check if the bot have those permissions if you want to run that command.'
            ))

    elif isinstance(error, commands.PrivateMessageOnly):
        await ctx.message.delete()
        await ctx.send('Sorry, but this command can only be used in DMs. '
                       'I have sent you a DM so you can get your message back.')
        await ctx.author.send('Sorry about that, but you can only use that command here. Here\'s the command you sent.')
        await ctx.author.send(f'```\n{ctx.message.content}```')

    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=discord.Embed(
            title='Command errored',
            description=f'There are required parameters missing!\n'
                        f'Check the usage of the command by doing `.h <command name>` and try again.'
        ))

    elif isinstance(error, commands.CommandInvokeError):
        embed = discord.Embed(
            title='Command errored',
            description=f'An unknown error happened!\n '
                        f'Don\'t worry, the developers have been notified. \n'
                        f'However, if you want to fix the problem yourself, the error will be included.'
        )
        embed.add_field(name='Error', value=str(error), inline=False)
        embed.add_field(name='Original Error', value=f'```python\n{error.original}```', inline=False)
        await ctx.send(embed=embed)

    elif isinstance(error, commands.NotOwner):
        await ctx.send(f'{ctx.author.mention} is not a sudoer. The incident will be reported.')

    elif isinstance(error, commands.BadArgument):
        await ctx.send(f'Bad Argument. Check your command and try again.\n Full error: ```\n{error}```')

    embed = discord.Embed(title='Error', description=f'```\n{error}```')
    embed.add_field(name='Server', value=f'{ctx.guild.name} ({ctx.guild.id})', inline=False)
    embed.add_field(name='User Responsible', value=f'{ctx.user.id} ({ctx.user.name})', inline=False)
    await bot.get_channel(675329366309208074).send('<@397029587965575170>', embed=embed)


# Run the bot
bot.run(token)
