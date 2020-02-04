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
        await ctx.send('This command is a work in progress. Check back in a while.')

#bans a user with a reason
@client.command()
@commands.has_any_role()
async def ban (ctx, member:discord.User=None, reason =None):
    if member == None or member == ctx.message.author:
        await ctx.channel.send("You cannot ban yourself")
        return
    if reason == None:
        reason = ""
    message = f"You have been banned from {ctx.guild.name} for {reason}"
    await member.send(message)
    # await ctx.guild.ban(member, reason=reason)
    await ctx.channel.send(f"{member} has been hit by the ban hammer..")

def setup(bot):
    bot.add_cog(GuildConfig(bot))
