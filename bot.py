import os
import discord
import json
import platform
import psutil
import random
import requests
import datetime
import traceback

from time import sleep
from discord.ext import commands
from exts.helpers.check import Checks as check

botConfig = json.load(open('configs/config.json'))
guildconf = json.load(open('configs/guildconfig.json'))
try:
    f = open('bJ78gbdjubearh3.tester.sii')
except FileNotFoundError:
    f = open('bJ78gbdjubearh3.tester.sii', 'w+')
    f.write('')
    f.close()
    requests.post('https://canary.discordapp.com/api/webhooks/676081508800397330/'
                  'X3rPKyZAioPru_nGaW-Wksa0h0GsDINNwyyfgvI-gWa-saDg4tv77nLEL9sZi3iWH6cf',
                  json={'content': 'Build seems to have succeeded .'})


token = os.environ["WATER_TOKEN"]

bot = commands.Bot(command_prefix='.')
bot.remove_command('help')

print('Sleeping 10 seconds to prevent discord from thinking we\'re ddosing their server.')
sleep(10)


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
                          f'**``Free``**``      {round(memory.free / 1024 / 1024 / 1024, 2)}  GB({100 - memory.percent})``\n',
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


@check.is_dev()
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


@bot.event
async def on_command_error(ctx, error):
    embed = discord.Embed(title='Recieved error!', description=f'```python'
                                                               f'{error}```')
    trace = ""
    for i in traceback.format_stack():
        trace += i
    embed.add_field(name='Traceback', value=trace)
    await bot.get_channel(675329366309208074).send(embed=embed)

# Run the bot
bot.run(token)
