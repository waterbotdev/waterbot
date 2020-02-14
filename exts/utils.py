import datetime, time
import platform, psutil
import random

import discord
from discord.ext import commands
from .helpers.util import TimeHelper as th


class Utils(commands.Cog):
    '''Utility commands
    '''

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='avatar', aliases=['av'])
    async def avatar(self, ctx, user: discord.Member = None):
        '''Avatar
        Get a user's/your avatar, with link.
        avatar [user mention]
        Send messages'''
        if user is None:
            user = ctx.message.author
        embed = discord.Embed(colour=user.colour)
        embed.set_author(name=f"{user}'s avatar")
        embed.set_image(url=user.avatar_url)
        embed.add_field(name="Avatar:", value=f"[Link]({user.avatar_url})")
        embed.set_image(url=str(user.avatar_url))
        embed.set_footer(text=f"User ID: {user.id}")
        await ctx.send(embed=embed)

    @commands.command()
    async def userinfo(self, ctx, member: discord.Member = None):
        '''Get member info
        Get the info of a user. Leave the command as is to check your own info.
        userinfo [UserID/Mention]
        Send messages'''
        status = ""
        if member is None:
            member = ctx.author
        # Find user roles.
        roles = [role for role in member.roles]
        # roles = roles.remove(roles[0])
        # roles.remove(0)
        embed = discord.Embed(color=member.color, timestamp=ctx.message.created_at)
        embed.set_author(name=f"User Information - {member.name}")
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="User ID:", value=member.id)
        embed.add_field(name="Created at:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
        embed.add_field(name="Joined at:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
        embed.add_field(name=f"Roles({len(roles)})", value=" ".join([role.mention for role in roles]))
        embed.add_field(name="Top Role:", value=[role.mention for role in [role for role in member.roles]][
            len([role.mention for role in [role for role in member.roles]]) - 1])
        embed.add_field(name="Is Bot User?", value=member.bot)
        embed.add_field(name="Animated Avatar", value=member.is_avatar_animated())
        embed.add_field(name="Avatar URL", value=f"[Avatar URL]({ctx.author.avatar_url})")
        if member.status == discord.Status.online:
            status = "<:Online:668360009960128522> Online"
        elif member.status == discord.Status.idle:
            status = "<:Idle:668360068206559232> Idle"
        elif member.status == discord.Status.dnd:
            status = "<:dnd:673084189066657792> Do Not Disturb"
        elif member.status == discord.Status.offline:
            status = "<:Invisible:668360216491982858> Invisible/Offline"
        embed.add_field(name="Status", value=status)
        await ctx.send(embed=embed)

    @commands.command()
    async def serverinfo(self, ctx, guild: discord.Guild=None):
        '''Get server info
        Get the info of a server.
        serverinfo [UserID/Mention]
        Send messages'''
        if guild is None:
            guild = ctx.guild
        embed = discord.Embed(color=ctx.author.color, timestamp=ctx.message.created_at)
        embed.set_author(name=f"Guild Name - {guild.name}")
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=guild.icon_url)
        embed.add_field(name="Guild ID", value=guild.id, inline=True)
        embed.add_field(name="Owner", value=guild.owner, inline=True)
        embed.add_field(name="Members", value=guild.member_count, inline=True)
        embed.add_field(name="Roles", value=guild.roles.name)
        embed.add_field(name="Categories", value=guild.categories)
        embed.add_field(name="Verification Level", value=guild.verification_level)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def boostinfo(self, ctx):
        '''Check the server's boost level
        Get the server's boost level\\n Altering boost level picture Soon:tm:
        boostinfo
        Send messages'''
        embed = discord.Embed(name=f"{ctx.message.guild.name}'s info", color=0xff5e81)
        embed.set_author(name=f"Nitro Boosting Status for: {ctx.message.guild.name}")
        embed.add_field(name="Boost Amount", value=ctx.message.guild.premium_subscription_count)
        embed.add_field(name="Boost / Server Level", value=ctx.message.guild.premium_tier)
        embed.set_footer(text=f"Requested By: {ctx.message.author}", icon_url=ctx.author.avatar_url)
        urls = {
            0: "https://cdn.discordapp.com/attachments/668332945748262933/668445394929319936/612036452779425792.png",
            1: "https://cdn.discordapp.com/attachments/668332945748262933/668445395411795977/612036451843964978.png",
            2: "https://cdn.discordapp.com/attachments/668332945748262933/668445394639781926/612036451873325076.png",
            3: "https://cdn.discordapp.com/attachments/668332945748262933/668445394317082634/612036451806478346.png"}
        featuresd = {"VIP_REGIONS": "VIP voice regions",
                     "VANITY_URL": "Vanity custom invite URL",
                     "INVITE_SPLASH": "Custom invite page background",
                     "VERIFIED": "Verified server",
                     "PARTNERED": "Parenered server",
                     "MORE_EMOJI": "Total Available emoji slots over 50",
                     "DISCOVERABLE": "Can be added to Server Discovery",
                     "COMMERCE": "Guild store channels",
                     "PUBLIC": "Users can lurk via Discovery",
                     "NEWS": "Guild news channels",
                     "BANNER": "Guild Banner",
                     "ANIMATED_ICON": "Animated Icon",
                     "PUBLIC_DISABLED": "Server can't be public"}
        embed.set_thumbnail(url=urls[ctx.guild.premium_tier])
        feat = "None"
        for i in ctx.guild.features:
            feat += f"{featuresd[i]} "
        embed.add_field(name="Server (Un)Features", value=feat, inline=False)
        await ctx.send(embed=embed)

    @commands.command(aliases=["wthr"])
    async def weather(self, ctx, *, loc):
        embed = discord.Embed(color=ctx.author.colour, timestamp=ctx.message.created_at)
        embed.set_image(url=f"https://wttr.in/{loc}.png?m%22")
        embed.set_author(name=f"Weather in {loc}")
        embed.set_footer(text=f"Requested By: {ctx.message.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name='sysinfo', aliases=['botinfo'])
    async def sysinfo(self, ctx):
        '''Check the bot's system info
        This command is used to check the bot's system info, such as CPU usage, RAM usage, etc.
        [sysinfo|botinfo]
        Send messages'''
        platd = platform.uname()
        memory = psutil.virtual_memory()
        color = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        embed = discord.Embed(title='Bot stats', description=f'Time: {datetime.datetime.now().__str__()}',
                              color=color)
        embed.add_field(name='CPU Usage', value=f'{psutil.cpu_percent()}%', inline=False)
        embed.add_field(name='Memory Usage',
                        value=f'**``Total``**``     {round(memory.total / 1024 / 1024 / 1024, 2)} GB``\n'
                              f'**``Available``**`` {round(memory.available / 1024 / 1024 / 1024, 2)} GB``\n'
                              f'**``Used``**``      {round(memory.used / 1024 / 1024 / 1024, 2)} GB({memory.percent})``\n'
                              f'**``Free``**``      {round(memory.free / 1024 / 1024 / 1024, 2)}  GB({100 - memory.percent})``\n',
                        inline=False)
        embed.add_field(name='Platform details', value=f'{platd.system} '
                                                       f'Release {platd.release} '
                                                       f'{platd.machine}\n', inline=False)
        embed.add_field(name='Uptime', value=th.sec_to_str(time.perf_counter()), inline=False)
        await ctx.send(embed=embed)

    @commands.command(name='ping')
    async def ping(self, ctx):
        '''Check the bot's latency
        Yes it checks the latency nothing more.
        ping
        Send messages'''
        latency = self.bot.latency * 1000
        if latency < 100:
            color = 0x55aa55
        elif latency < 500:
            color = 0xffff55
        else:
            color = 0xff5555
        initt = time.perf_counter()
        msg = await ctx.send(embed=discord.Embed(description=f'Ping! Latency: {latency}', color=color))
        roundt = time.perf_counter() - initt
        await msg.edit(embed=discord.Embed(description=f'Ping! Latency: {round(latency, 4)} ms\n'
                                                       f'Message Roundtrip latency: {round(roundt * 1000, 4)} ms',
                                           color=color))


def setup(bot):
    bot.add_cog(Utils(bot))
