import discord
from discord.ext import commands


class AutoRespond(commands.Cog):
    '''Autorespond cog, can be disabled'''
    def __init__(self, bot):
        self.bot = bot




def setup(bot):
    bot.add_cog()