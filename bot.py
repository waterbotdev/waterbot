import discord
# import random
# import requests
# import json
import os
from discord.ext import commands
token = os.environ["BOT_TOKEN"]
bot = commands.Bot(command_prefix='.')

bot.remove_command('help')


@bot.event
async def on_ready():
    print(f'Logged in as: {bot.user.name}')
    print(f'With ID: {bot.user.id}')

# This command had to stay or else i am ready to kill the whole bot.
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

# Used extentions because why not.
cogs = [
    'exts.core',
    'exts.fun',
    'exts.utils'
    ]
if __name__ == '__main__':
    for cog in cogs:
        bot.load_extension(cog)

# Run the bot
bot.run(token)
