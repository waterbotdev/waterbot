import discord
from discord.ext import commands


class Core(commands.Cog):
    '''Core commands
    '''
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def invite(self,ctx):
        '''Sends the invite of the bot to a text channel
        '''
        embed=discord.Embed(title="Invite Waterbot", url="https://cdn.discordapp.com/avatars/655262203309719552/ca12b1a43ea265c81535b83fb4d6fb21.png?size=128", description="use this link to add waterbot to your server!", color=0x8cff8f)
        embed.set_author(name="waterbot", url="https://cdn.discordapp.com/avatars/655262203309719552/ca12b1a43ea265c81535b83fb4d6fb21.png?size=128")
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/655262203309719552/ca12b1a43ea265c81535b83fb4d6fb21.png?size=128")
        embed.add_field(name="https://discordapp.com/api/oauth2/authorize?client_id=655262203309719552&permissions=8&scope=bot", value="waterbot", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def activity(self,ctx,*,text):
        '''Sets the bots status (OWNER)
        Usage: activity <Status Text>
        '''
        game = discord.Game(text)
        await ctx.bot.change_presence(status=discord.Status.online, activity=game)
        await ctx.send(':ok_hand: Done.')
    @activity.error
    async def activityError(self,ctx,error):
        await ctx.send("Command errored.\n{}".format(error))

    @commands.command(name='say')
    @commands.has_permissions(manage_messages=True)
    async def say(self,ctx, *, text):
        '''Make the bot say something
        Usage: say <text>
        You need to have the manage messages permisson to do this.
        '''
        await ctx.send(text)

    # Error handler of the say command
    @say.error
    async def sayError(self,ctx,error):
        await ctx.send("Command errored.\n{}".format(error))


    @commands.command(name="help", aliases=['h'])
    async def help(self, ctx, command: str = None):
        '''Help command
        Usage: help [command]
        This command only include available extensions/cogs/categories, and
        '''
        if command is None:
            cognames = []
            for i in ctx.bot.commands:
                if i.cog_name not in cognames:
                    cognames.append(i.cog_name)
            out = "`"
            for i in cognames:
                out += f"{i}\n"
            out += "`"
            embed = discord.Embed(title="Waterbot Help",description='Use .cmds <category name>` to get the available commands in a category', colour=0xfffbb)
            embed.add_field(name="Available modules of waterbot", value=out)
            embed.set_footer(text="Remove `<>` and `[]`s when using a command.")
            return await ctx.send(embed=embed)
        else:
            await ctx.send("Not implemented yet.")

    # TODO: LIST COMMANDS IN A MODULE
    @commands.command(name="cmds")
    async def cmds(self, ctx, cog=None):
        '''List commands available in an extension
        Usage: cmds <category name>
        '''
        # Grab the command list
        cmds = {}
        for i in ctx.bot.commands:
            if i.cog_name not in cmds:
                cmds[i.cog_name] = []
                cmds[i.cog_name+'_des'] = i.cog.description
            cmds[i.cog_name].append(ctx.bot.command_prefix+i.name)
        if cog not in cmds:
            return await ctx.send(embed=discord.Embed(description=f"No such category({cog}).",colour=0xff5555))
        out = "`"
        for i in cmds[cog]:
            out += f"{i}\n"
        embed = discord.Embed(title=f"Commands in category `{cog}`",colour=0xa12ba1)
        embed.add_field(name="Category description", value=f"`{cmds[cog+'_des'].splitlines()[0]}`",inline=False)
        embed.add_field(name="Available commands", value=f"{out}`", inline=False)
        return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Core(bot))
