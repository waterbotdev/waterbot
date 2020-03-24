import json
import datetime

import discord
from discord.ext import commands

from enum import Enum


class TimeHelper:
    """Useful module for converting times and shit.
    """

    @staticmethod
    def str_to_sec(tst):
        """
        Converts Half-readable text format into seconds

        :param tst: Text time format (#y#mo#w#h#m#s) (No space)
        :return: seconds[int]
        """

    @staticmethod
    def sec_to_str(sec):
        """
        Convert Seconds to readable text format

        :param sec: Seconds
        :return:
        """
        m = 0
        h = 0
        d = 0
        s = sec
        while s >= 86400:
            d += 1
            s -= 86400
            # print(f'Add D \tS:{s}\t{d}d\t{h}h\t{m}m\t{s}s', end='\r')
        while s >= 60 * 60:
            h += 1
            s -= 60 * 60
            # print(f'Add S \tS:{s}\t{d}d\t{h}h\t{m}m\t{s}s', end='\r')
        while s >= 60:
            m += 1
            s -= 60
            # print(f'Add M \tS:{s}\t{d}d\t{h}h\t{m}m\t{s}s', end='\r')
        return f'{d}d {h}h {m}m {s}s'


class DbS(Enum):
    MUTES = 'dbs/mutes.json'
    KICKS = 'dbs/kicks.json'
    BANS = 'dbs/bans.json'
    LOGS = 'dbs/logs.json'
    GUILDS = 'dbs/guild.json'

# Exceptions
class ModExceptions:
    class MemberNotFound(Exception):
        pass

    class HierarchyError(Exception):
        pass

class DBExceptions:
    class ConfigNotFoundError(Exception):
        pass

class DB:
    """Database commands"""

    @staticmethod
    def addlog(uid: int, timestamp: int, item: str, description: str, modrid: int, end: int = None):
        """
        Add a log object to the json database

        :param uid: User ID.
        :param timestamp: The timestamp that the item is recorded.
        :param item: The item that user infracted(mute, kick, ban, warn)
        :param description: Descriptions of the action, also includes different parameters, for specific types.
        :param modrid: Moderator responsible
        :param end:
        :return: None
        """
        types = ['warn', 'mute', 'kick', 'tempban', 'ban']
        if item not in types:
            raise TypeError(f'Type {item} is not in the acceptable '
                            f'list.')
        file = open(DbS.LOGS.value, 'r')
        logs = json.load(file)
        file.close()
        if uid not in logs:
            logs[uid] = []
        logs[uid].append({
            "time": timestamp,
            "cate": item,
            "desc": {},
            "modr": modrid
        })
        logs[uid][len(logs[uid]) - 1]['desc']['reason'] = description
        if item == 'mute':
            if end is None:
                raise TypeError('"end" parameter does not have a value when using "mute" type')
            logs[uid][len(logs[uid]) - 1]['desc']['start'] = timestamp
            logs[uid][len(logs[uid]) - 1]['desc']['end'] = timestamp + end
        elif item == 'tempban':
            logs[uid][len(logs[uid] - 1)]['desc']['start'] = timestamp
            logs[uid][len(logs[uid]) - 1]['desc']['end'] = timestamp + end

    @staticmethod
    def addmute(uid: int, seconds: int, reason: str):
        """
        Add a mute record for a user

        :param uid: User ID
        :param seconds: Seconds for the mute(either calculated by hand/code or by TimeHelper.tosec()
        :param reason: Reason to be muted
        :return: None
        """
        file = open(DbS.MUTES.value, 'r')
        mutes = json.load(file)
        mutes['uid'] = datetime.datetime.now().timestamp() + seconds

    @staticmethod
    def get_guild_config(gid: int):
        """
        Get the configurations for a guild. This will somehow make life easier.

        :param gid: Guild ID
        :return: guildconfig[dict]
        :exception ConfigNotFoundError: The config file for the guild is no found.
        """
        config = ""
        with open(DbS.GUILDS.value, 'r') as c:
            conf = json.load(c)
            try:
                config = conf[gid]
            except KeyError:
                raise DBExceptions.ConfigNotFoundError(f'Config entry for guild {gid} does not exist.')
        return config


def can_execute_action(ctx, user, target):
    #      ||         is_Owner         ||      is_Guild_Owner     ||           RoleHigher          |
    return user.id == ctx.bot.owner_id or user == ctx.guild.owner or user.top_role > target.top_role


# AUTHOR: RAPPTZ
def cleanup_code(content):
    """
    Automatically remove code blocks from the code.

    :param content: The object to clean up
    :return: Cleaned up code
    """
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])
    else:
        return content


# AUTHOR: RAPPTZ
def get_syntax_error(self, e):
    _ = self
    if e.text is None:
        return f'```py\n{e.__class__.__name__}: {e}\n```'
    return f'```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}: {e}```'


async def resolve_member(guild, member_id):
    member = guild.get_member(member_id)
    if member is None:
        if guild.chunked:
            raise ModExceptions.MemberNotFound()
        try:
            member = await guild.fetch_member(member_id)
        except discord.NotFound:
            raise ModExceptions.MemberNotFound() from None
    return member


class Converters:
    # Converters

    class Member(commands.Converter):
        async def convert(self, ctx, argument):
            member_id = ""
            try:
                m = await commands.MemberConverter().convert(ctx, argument)
            except commands.BadArgument:
                try:
                    member_id = int(argument, base=10)
                    m = await resolve_member(ctx.guild, member_id)
                except ValueError:
                    raise commands.BadArgument(f"{argument} is not a valid member or member ID.") from None
                except ModExceptions.MemberNotFound:
                    return type('IDUser', (), {
                        'id': member_id,
                        '__str__': lambda s: f'Member ID {s.id}',
                        'mention': f'<@{member_id}>',
                        '__type__': 'IDUser'
                    })()
            if not can_execute_action(ctx, ctx.author, m):
                raise ModExceptions.HierarchyError('You cannot do this action on this user.')
            return m
