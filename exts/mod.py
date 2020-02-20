import json
import discord
from discord.ext import commands, tasks
from .helpers.util import *

botconf = json.load(open('configs/config.json'))


# noinspection PyShadowingNames
class Mod(commands.Cog):
    '''Moderation Commands'''

    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(manage_messages=True, manage_roles=True)
    @commands.command(name='mute')
    async def mute(self, ctx, users: commands.Greedy[discord.Member], duration: str = '30m',
                   reason: str = "No Reason Given."):
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
    async def ban(self, ctx, members: commands.Greedy[Converters.Member], delete_days: str = '1d', *,
                  reason: str = "None"):
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

    @commands.has_permissions(manage_roles=True)
    @commands.command(name='addrole', aliases=['addrole'])
    async def addrole(self, ctx, users: commands.Greedy[discord.Member], rolename: str):
        '''Add a role to user
        Adds a role to users, with id/ping.
        addrole <user mentions> <said role's **name**>'''
        role = discord.utils.find(lambda a: a.name == rolename, ctx.guild.roles)
        success = []
        failed = []
        if len(users) == 0:
            return await ctx.send('')
        if role is None:
            return await ctx.send('Role not found. Please check your spellings and try again. It is CaSe-SeNsItIvE!')
        async with ctx.channel.typing():
            for i in users:
                try:
                    await i.add_roles(role)
                except Exception as e:
                    failed.append(i.mention + " ")
                else:
                    success.append(i.mention + " ")

        sstr, fstr = "", ""
        for i in success:
            sstr += i
        for i in failed:
            fstr += i
        embed = discord.Embed(title=f'Added roles for {len(success)} user(s)', description=f'Role: {role.name}')
        if len(success) != 0:
            embed.add_field(name='Successfully added for', value=sstr)
        if len(failed) != 0:
            embed.add_field(name='Failed to add for', value=fstr)
        await ctx.send(embed=embed)

    # LOOPING TASKS #

    @tasks.loop(seconds=10)
    async def unmuteloop(self):
        '''Check if any users is ok for unmuting.
        '''
        mutelist = open('dbs/mutes.json')


def setup(bot):
    bot.add_cog(Mod(bot))
