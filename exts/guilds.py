import discord
from discord.ext import commands

import json


class GuildConfig(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @commands.command(name='loadconfig', aliases=['loadconf'])
    async def loadconfig(self, ctx, *, json: str):
        '''Load server config
        Load a server config file from text.\\nSupport for file input will be supported later.
        loadconfig <config json>
        Server administrator'''
        await ctx.send(f'This command is a work in progress. Check back in a while.\n '
                       f'{json}')

def setup(bot):
    bot.add_cog(GuildConfig(bot))
