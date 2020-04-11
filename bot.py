import os
import json
import psutil
import random
import discord
import logging
import platform
import datetime
import traceback

from time import sleep
from discord.ext import commands
from exts.helpers.util import DB, DBExceptions

# Configurations
logging.basicConfig(level=logging.INFO)
botConfig = json.load(open('config.json'))

token = os.environ["WATER_TOKEN"]


def get_prefix(client, message):
    return '.'


bot = commands.AutoShardedBot(command_prefix=get_prefix, case_insensitive=True, owner_ids=[
    513603936033177620,  # Dragonic
    397029587965575170,  # Kenny
    521656100924293141,  # Zac
    374047038926618624])  # Lindsey
bot.remove_command('help')

print('Sleeping 10 seconds to prevent discord from thinking we\'re ddosing their server.')
sleep(10)


# noinspection DuplicatedCode
@bot.event
async def on_ready():
    # revision = subprocess.run(['git', 'rev-list', '--all', '--max-count=1'], stdout=subprocess.PIPE)
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
    # embed.add_field(name="Git revision", value=revision.stdout.decode())
    await bot.get_channel(botConfig['startchannel']).send(embed=embed)


# Used extentions because why not.
cogs = [
    'exts.core',
    'exts.fun',
    'exts.utils',
    'exts.dev',
    'exts.mod',
    'exts.passives'
]
if __name__ == '__main__':
    for cog in cogs:
        bot.load_extension(cog)


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
        ).add_field(
            name='Error',
            value=f'```py\n{error}```'
        ))

    elif isinstance(error, commands.CommandInvokeError):
        embed = discord.Embed(
            title='Command errored',
            description=f'An unknown error happened!\n '
                        f'Don\'t worry, the developers have been notified. \n'
                        f'However, if you want to fix the problem yourself, the error will be included.'
        )
        embed.add_field(name='Error', value=str(error), inline=False)
        embed.add_field(name='Original Error', value=f'```py\n{error.original}```', inline=False)
        await ctx.send(embed=embed)

    elif isinstance(error, commands.NotOwner):
        await ctx.send(f'{ctx.author.mention} is not a sudoer. The incident will be reported.')

    elif isinstance(error, commands.BadArgument):
        await ctx.send(f'Bad Argument. Check your command and try again.\n Full error: ```\n{error}```')

    elif isinstance(error, commands.CommandNotFound):
        await bot.get_channel(675329366309208074).send('\n'
                                                       'CommandNotFound\n'
                                                       f'Dipshit to detention: {ctx.author.id} ({ctx.author.name})')
        return

    embed = discord.Embed(title='Error', description=f'```\n{error}```')
    embed.add_field(name='Server', value=f'{ctx.guild.name} ({ctx.guild.id})', inline=False)
    embed.add_field(name='User Responsible', value=f'{ctx.author.id} ({ctx.author.name})', inline=False)
    with open('exception.txt', 'w+') as tempexceptionfile:
        tempexceptionfile.write("".join(traceback.TracebackException.from_exception(error).format()))
    file = discord.File('exception.txt')
    await bot.get_channel(675329366309208074).send('<@&686449668648861786>', embed=embed, file=file)


# Run the bot
bot.run(token)
