import os
import discord
import json
from discord.ext import commands
from exts.helpers.check import Checks as check

botConfig = json.load(open('config.json'))
guildconf = json.load(open('guildconfig.json'))

token = os.environ["WATER_TOKEN"]

bot = commands.Bot(command_prefix='.')
bot.remove_command('help')


@bot.event
async def on_ready():
    print(f'Logged in as: {bot.user.name}')
    print(f'With ID: {bot.user.id}')


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
                    channel = bot.get_channel(guildconf[i]['joinchannel'])
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
                    channel = bot.get_channel(guildconf[i]['leavechannel'])
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
            bot.unload_extension(i)
            print(f'Unloaded extension {i}')
            log += f'Unloaded extension {i}\n'
        except Exception as e:
            print(e)
            pass
        bot.load_extension(i)
        print(f'Loaded extension {i}')
    await ctx.send(log)


# Run the bot
bot.run(token)
