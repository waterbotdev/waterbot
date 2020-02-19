import json
import discord
from discord.ext import commands, tasks

botconf = json.load(open('configs/config.json'))


# Exceptions
class ModExceptions:
    class MemberNotFound(Exception):
        pass


# Converters?

def can_execute_action(ctx, user, target):
    #      ||         is_Owner         ||      is_Guild_Owner     ||           RoleHigher          |
    return user.id == ctx.bot.owner_id or user == ctx.guild.owner or user.top_role > target.top_role


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
            raise commands.BadArgument('You cannot do this action on this user due to role hierarchy.')
        return m


# noinspection PyShadowingNames
class Mod(commands.Cog):
    '''Moderation Commands'''

    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(manage_messages=True, manage_roles=True)
    @commands.command(name='mute')
    async def mute(self, ctx, users: commands.Greedy[discord.Member], duration: str = '30m', reason: str = "No Reason Given."):
        '''Mute a user
        Mute a user to their mute jail cell\\nWho told them to misbehave, do this when you need to, but not abuse it.
        mute <user> [Reason]
        Manage messages, Manage roles'''
        # await ctx.send('Connecting...',delete_after=4)
        reason = f"Executed by user {ctx.author} | Reason: {reason}"
        mute = discord.utils.get(ctx.guild.roles, name="Muted")
        if mute is None:
            mute = discord.utils.get(ctx.guild.roles, name="muted")
        async with ctx.channel.typing():
            for i in users:
                await i.add_roles(mute, reason=reason)
        embed = discord.Embed(title='User(s) muted.')
        await ctx.send(embed=embed)

    # @mute.error
    # async def mute_error(self, error, ctx):
    #     '''The errors that the mute command made'''
    #     ## DISABLED

    @commands.has_permissions(manage_messages=True)
    @commands.command(name='prune', aliases=['remove', 'clear', 'purge'])
    async def prune(self, ctx, amount: int, members: commands.Greedy[discord.Member] = None):
        '''Clear messages
        Clear a number of messages, either globally or just from a user.
        [prune|remove|clear] <amount of messages> [User mention(s)]
        Manage Messages'''
        time = ctx.message.created_at
        await ctx.message.delete()
        users = ''
        if members is not None:
            def check(m):
                for i in members:
                    if m.author == i:
                        return True
                    else:
                        pass
                return False

            try:
                ret = await ctx.channel.purge(limit=amount, check=check)
            except Exception as e:
                return await ctx.send(embed=discord.Embed(title='Command Errored.', description=e))
            for i in members:
                users += i.mention
        else:
            try:
                ret = await ctx.channel.purge(limit=amount)
            except Exception as e:
                return await ctx.send(embed=discord.Embed(title='Command Errored.', description=e))
        sornah = "s" if len(ret) > 1 else ""
        embed = discord.Embed(description=f'Deleted {len(ret)} message{sornah} '
                                          f'{f"from {users}" if users != "" else ""}',
                              timestamp=time)
        embed.set_footer(text='This message will be deleted in 5 seconds.')
        await ctx.send(embed=embed, delete_after=5)

    @commands.has_permissions(ban_members=True)
    @commands.command(name='ban')
    async def ban(self, ctx, members: commands.Greedy[Member], delete_days: str = '1d', *, reason: str = "None"):
        '''Ban users
        Mass bans members with a delete_days parameter.\\n**HOW TO USE THE DELETE_DAYS PARAMETER**:\\n #y#mo#w#h#m#s (i.e. 3y for 3 years, 2mo3h14m for 2 months, 3 hours and 14 minutes) \\ny=Year mo=Month w=Week h=Hour m=Minute s=Second
        ban <member pings/ids> <delete days> <reason>
        Ban members'''
        member = ""
        for i in members:
            member += i.mention + " "
        for member in members:
            if member.__type__ == 'IDUser':
                await ctx.guild.ban(member, reason=reason)
            else:
                await member.ban(delete_message_days=delete_days, reason=reason)
        embed = discord.Embed(title=f'{len(members)} member(s) banned.')
        embed.add_field(name='Amount', value=str(len(members)))
        embed.add_field(name='Members', value=member)
        embed.add_field(name='Reason', value=reason, inline=False)
        await ctx.send(embed=embed)

    @commands.has_permissions(kick_members=True)
    @commands.command(name='kick')
    async def kick(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):
        '''Kick a user from the server
        Kick a bad user from the guild.
        kick <members> [reason]'''
        membs = ""
        if reason is None:
            reason = 'None given.'
        for i in members:
            membs += i.mention
            await i.kick(reason=f'Responsible user: {ctx.author}|reason: {reason}')
        await ctx.send(f"{ctx.author} Successfully kicked {len(members)}(`{membs}`)  member(s), with reason {reason}")

    # LOOPING TASKS
    @tasks.loop(seconds=10)
    async def unmuteloop(self):
        '''Check if any users is ok for unmuting.
        '''
        mutelist = open('dbs/mutes.json')


def setup(bot):
    bot.add_cog(Mod(bot))
