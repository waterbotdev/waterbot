import discord
# import random
# import requests
# import json
import os
from discord.ext import commands
token = os.environ["WATER_TOKEN"]
bot = commands.Bot(command_prefix='.')

# bot.remove_command('help')


@bot.event
async def on_ready():
    print(f'Logged in as: {bot.user.name}')
    print(f'With ID: {bot.user.id}')

# # This command had to stay here or else i am ready to kill the whole bot.
# @bot.command()
# async def help(ctx):
#     '''Help command
#     '''

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

# Run the bot
bot.run(token)
