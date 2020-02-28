from google import google
import discord
from discord.ext import commands


class Search(commands.Cog):
    '''Searcg Cog'''

    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def google(self, ctx):
        '''Parent command for google search commands
        This command will list all the subcommands for the google group.
        google [subcommand]
        Send messages'''


def setup(bot):
    bot.add_cog(Search(bot))
