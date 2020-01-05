import discord
import re
from discord.ext import commands

class Core(commands.Cog):
    '''Core commands
    '''
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def invite(self,ctx):
        '''Sends a link to invite the bot to your server
        Self-explanatory
        invite
        None'''
        embed=discord.Embed(title="Invite Waterbot", url="https://cdn.discordapp.com/avatars/655262203309719552/ca12b1a43ea265c81535b83fb4d6fb21.png?size=128", description="use this link to add waterbot to your server!", color=0x8cff8f)
        embed.set_author(name="waterbot", url="https://cdn.discordapp.com/avatars/655262203309719552/ca12b1a43ea265c81535b83fb4d6fb21.png?size=128")
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/655262203309719552/ca12b1a43ea265c81535b83fb4d6fb21.png?size=128")
        embed.add_field(name="https://discordapp.com/api/oauth2/authorize?client_id=655262203309719552&permissions=8&scope=bot", value="waterbot", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def activity(self,ctx,*,text):
        '''Sets the bots status
        Set the bot's playing status
        activity <Status Text>
        Bot Owner only'''
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
        Self-explanatory
        say <text>
        Manage Messages'''
        await ctx.send(text)

    # Error handler of the say command
    @say.error
    async def sayError(self,ctx,error):
        await ctx.send(f"Command errored.\n{error}")

    @commands.has_permissions(manage_messages=True)
    @commands.command()
    async def sayembed(self, ctx, *, param):
        '''Make the bot say something
        Make the bot say something in embeds. \\nColor have to be a rgb integer number(155012074) \\nMkae sure not to put ANY `|` in your text or else the code won't work.
        sayembed <body>|[color]|[title]|[footer]
        Manage Messages'''
        sppar = param.split('|')
        body = None
        color = 0
        title = None
        footer = None
        try:
            body = sppar[0]
            color = sppar[1]
            title = sppar[2]
            footer = sppar[3]
        except Exception as e:
            pass
        if color is not None:
            if len(color) is 9:
                color = discord.Colour.from_rgb(int(color[0]+color[1]+color[2]), int(color[3]+color[4]+color[5]), int(color[6]+color[7]+color[8]))
            else:
                return ctx.send(embed=discord.Embed(title='Command Errored',
                                                    description='Color must be a 9 digit RGB integer code\n e.g. `#0F13B4` would be `015019180`.Make sure there\'s **NO** spaces between them and try again.',
                                                    timestamp=ctx.message.created_at)
                                .set_footer(text='This message will self-destruct in 5 seconds.'))
        embed = discord.Embed(title=title,description=body)
        if footer is not None:
            embed.set_footer()
        await ctx.send(embed=embed)

    @sayembed.error
    async def sayembederror(self, ctx, error):
        await ctx.send(f"Command errored. \n{error}")

    @commands.command(name="help", aliases=['h'])
    async def help(self, ctx, command: str = None):
        '''Help command
        This command only include available extensions/cogs/categories, and in-depth explanations of the specified command.
        help [command name]
        None
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
            stat = 0
            result = None
            for i in ctx.bot.commands:
                if i.name == command:
                    stat = 1
                    result = i
                    break
            if stat == 0:
                return ctx.send(embed=discord.Embed(description=f"No such command. ({command}) Use .help to list all available modules and use .cmds <module name> to check the available commands in that module.", colour=0xff5555))
            else:
                doc = result.help.splitlines()
                embed = discord.Embed(title=f"Help for command {command}", colour=0xa12ba1)
                embed.add_field(name="Short Description",value=doc[0])
                embed.add_field(name="Usage",value=ctx.bot.command_prefix+doc[2])
                embed.add_field(name="Main Help", value=re.sub('\\n','\n',doc[1]))
                embed.add_field(name="Command Checks",value=doc[3])
            await ctx.send(embed=embed)
    @commands.command(name="cmds")
    async def cmds(self, ctx, cog=None):
        '''List commands available in an extension
        List all commands in an extension/category
        cmds <category name>
        None
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
