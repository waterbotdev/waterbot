import discord
from discord.ext import commands

class Utils(commands.Cog):
    '''Utility commands
    '''
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name='ping')
    async def ping(self,ctx):
        '''Get the bot latency
        Also used to check if bot is online.
        ping
        None'''
        botping = ctx.bot.latency*1000
        if botping < 100:
            color = 0x55aa55
        elif botping < 500:
            color = 0xffff55
        else:
            color = 0xff5555
        await ctx.send(embed=discord.Embed(description=f"Bot ping: {botping}",colour=color))

    @commands.command(name='avatar',aliases=['av'])
    async def avatar(ctx, user: discord.Member=ctx.message.author):
        embed = discord.Embed(colour=user.colour)
        embed.set_author(name=f"{user}'s avatar")
        embed.set_image(url=user.avatar_url)
        embed.add_field(name="Avatar:", value=f"[Link]({user.avatar_url})")
        
        embed.set_image(url=str(user.avatar_url))
        embed.set_footer(text=f"User ID: {user.id}")
    
        await ctx.send(embed=embed)
        
    @commands.command()
    async def userinfo(self,ctx,member:discord.Member=None):
        '''Get member info
        Get the info of a user. Leave the command as is to check your own info.
        userinfo [UserID/Mention]
        None'''
        if member == None:
            member = ctx.author
        # Find user roles.
        roles = [role for role in member.roles]
        #roles = roles.remove(roles[0])
        #roles.remove(0)
        embed = discord.Embed(color=member.color, timestamp=ctx.message.created_at)
        embed.set_author(name=f"User Information - {member.name}")
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="User ID:", value=member.id)
        embed.add_field(name="Created at:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
        embed.add_field(name="Joined at:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
        embed.add_field(name=f"Roles({len(roles)})", value=" ".join([role.mention for role in roles]))
        embed.add_field(name="Top Role:", value=[role.mention for role in [role for role in member.roles]][len([role.mention for role in [role for role in member.roles]])-1])
        embed.add_field(name="Is Bot?",  value=member.bot)

        await ctx.send(embed=embed)

    @commands.command()
    async def boostinfo(self,ctx):
        '''Check the server's boost level
        None
        boostinfo
        None'''
        embed = discord.Embed(name="{}'s info".format(ctx.message.guild.name), color=0xd399f0)
        embed.set_author(name=f"Nitro Boosting Status for: {ctx.message.guild.name}")
        embed.add_field(name="Boost Amount", value=ctx.message.guild.premium_subscription_count)
        embed.add_field(name="Boost / Server Level", value=ctx.message.guild.premium_tier)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/571045753091522607/618829850656112650/Excalibur.png")
        embed.set_footer(text=f"Requested By: {ctx.message.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Utils(bot))
