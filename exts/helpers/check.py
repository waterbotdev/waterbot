import json
from discord.ext import commands

config = json.load(open('configs/config.json'))


class Checks:
    @staticmethod
    def is_dev():
        async def predicate(ctx):
            return ctx.author.id in config["developers"]

        return commands.check(predicate)

    @staticmethod
    def role_hierarchy():
        async def predicate(ctx):
            return user.id == ctx.bot.owner_id or \
                user == ctx.guild.owner or \
                    user.top_role > target.top_role
        return commands.check(predicate)
