import discord
from discord.ext import commands

devs = [
    513603936033177620,
    513603936033177620,
    397029587965575170
]

class checks():
    def is_dev():
        async def predicate(ctx):
            return ctx.author.id in devs
        return commands.check(predicate)
