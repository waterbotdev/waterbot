import json
from discord.ext import commands

config = json.load(open('configs/config.json'))


class Checks:
    @staticmethod
    def is_dev():
        async def predicate(ctx):
            return ctx.author.id in config["developers"]

        return commands.check(predicate)
