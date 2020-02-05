import json
import discord
from discord.ext import commands

botconf = json.load(open('config.json'))


# noinspection PyShadowingNames
class Mod(commands.Cog):
    '''Moderation Commands'''

    def __init__(self, bot):
        self.bot = bot
        
    @commands.has_oermissions(manage_messages=True, manage_roles=True)
    @commands.command(name='mute')
    async def mute(self, ctx, user: discord.Member, reason: str = "none"):
        guild = ctx.guild
        
        for role in guild.roles :
            if role.name == "Muted"
                await member.add_roles(role)
                await ctx.send(f"`{member.name}` has been muted. {reason}")
                return
            
                overwrite = discord.PermissionsOverwrite(send_message=False)
                newRole = await guild.create_role(name="Muted")
                
                for channel in guild.text_channels:
                    await channel.set_permissions(newRole,overwrite=overwrite)
                    
                await member.add_roles(newRole)
                await ctx.send(f"`{member.name}` has been muted. {reason}")

    @commands.has_permissions(manage_messages=True)
    @commands.command(name='prune', aliases=['remove', 'clear'])
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
        embed = discord.Embed(description=f'Deleted {len(ret)} message{sornah} {f"from {users}" if users != "" else ""}'
                              , timestamp=time)
        embed.set_footer(text='This message will be deleted in 5 seconds.')
        await ctx.send(embed=embed, delete_after=5)

    @commands.has_permissions(ban_members=True)
    @commands.command(name='ban')
    async def ban(self, ctx, members: commands.Greedy[discord.Member], delete_days:int, *, reason: str):
        '''Ban users
        Mass bans members with a delete_days parameter
        ban <member pings> <delete days> <reason>
        Ban members'''
        for member in members:
            await member.ban(delete_message_days=delete_days, reason=reason)

    @commands.has_permissions(kick_members=True)
    @commands.command(name='kick')
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f"Sucesfully kicked `{member.name}`.")

    @mute.error
    @prune.error
    @ban.error
    @kick.error
    async def moderr(self, ctx, error):
        await ctx.send(embed=discord.Embed(title='Command errored.', description=error))


def setup(bot):
    bot.add_cog(Mod(bot))
