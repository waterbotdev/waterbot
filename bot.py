import os
import discord
import json
from discord.ext import commands

botConfig = json.load(open('config.json','r'))
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
    'exts.dev'
    ]
if __name__ == '__main__':
    for cog in cogs:
        bot.load_extension(cog)


def is_dev():
    async def predicate(ctx):
        return ctx.author.id in botConfig["developers"]
    return commands.check(predicate)

@is_dev()
@bot.command()
async def reload(self, ctx):
    '''Reload all extensions
    Usage: reload
    '''
    for i in cogs:
        try:
            bot.unload_extension(i)
            print(f'Unloaded extension {i}')
        except Exception as e:
            print(e)
            pass
        bot.load_extension(i)
        print(f'Loaded extension {i}')


# Run the bot
bot.run(token)
