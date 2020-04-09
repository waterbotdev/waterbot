import logging
import discord
from discord.ext import commands


class Functions:
    @staticmethod
    def get_item(name, obj):
        """
        Get the value of an item in a dict

        :param name: The name of the item
        :param obj: The dict to search things from
        :return: None, Any
        """
        if type(obj) != dict:
            raise NotImplementedError('Not a dict.')
        if name not in obj:
            return None
        else:
            return obj[name]

    @classmethod
    def get_prefix(cls, bot, message):
        botid = bot.user.id
        avail = [f'<@{botid}>', f'<@!{botid}']  # Allow pinging the bot as a prefix.
        if message.guild is None:  # Not in a guild
            avail.append('.')
        else:
            avail.extend(cls.get_item(str(message.guild.id), bot.prefixes))


class Waterbot(commands.AutoShardedBot):
    def __init__(self):
        self.fns = Functions()
        super().__init__(command_prefix=self.fns.get_prefix)

