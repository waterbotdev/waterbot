import discord
from discord.ext import commands

class Core(commands.Cog):
    '''Core commands
    '''
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def invite(ctx):
        embed=discord.Embed(title="Invite Waterbot", url="https://cdn.discordapp.com/avatars/655262203309719552/ca12b1a43ea265c81535b83fb4d6fb21.png?size=128", description="use this link to add waterbot to your server!", color=0x8cff8f)
        embed.set_author(name="waterbot", url="https://cdn.discordapp.com/avatars/655262203309719552/ca12b1a43ea265c81535b83fb4d6fb21.png?size=128")
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/655262203309719552/ca12b1a43ea265c81535b83fb4d6fb21.png?size=128")
        embed.add_field(name="https://discordapp.com/api/oauth2/authorize?client_id=655262203309719552&permissions=8&scope=bot", value="waterbot", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def activity(ctx,*,text):
        """Sets the bots status (OWNER)"""
        #await ctx.send(content=" :ok_hand: What is the message you want in status")
        #message = await client.wait_for('message')
        #game = discord.Game(message.content)
        game = discord.Game(text)
        await bot.change_presence(status=discord.Status.online, activity=game)
        await ctx.send(':ok_hand: Done.')
    @activity.error
    async def activityError(ctx,error):
        await ctx.send("Command errored.\n{}".format(error))

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def say(ctx, *, text):
        '''Make the bot say something
        You need to have the manage messages permisson to do this.
        '''
        await ctx.send(text)
    @say.error
    async def sayError(ctx,error):
        await ctx.send("Command errored.\n{}".format(error))
def setup(bot):
    bot.add_cog(Core(bot))
