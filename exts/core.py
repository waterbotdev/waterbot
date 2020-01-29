import discord
import re
from .helpers.check import Checks
from discord.ext import commands


class Core(commands.Cog):
    '''Core commands
    '''

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def invite(self, ctx):
        '''Sends a link to invite the bot to your server
        Self-explanatory
        invite
        Send messages'''
        embed = discord.Embed(color=ctx.author.colour, url="https://discordapp.com",
                              description="Waterbot is a bot to invite to your Discord server to have a nice environment in the community. We offer highly, easy ~~meme~~ commands for everyone to use. Such as moderation, fun command and even more nonsense, If you want to add Waterbot to your server, click the following link.\n\n**[Click here to add Waterbot](https://discordapp.com/api/oauth2/authorize?client_id=655262203309719552&permissions=8&scope=bot)**")
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/618797799655473201/619221825687257088/568466408548335650.png")
        embed.set_author(name="Invite Waterbot", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                         icon_url="https://cdn.discordapp.com/avatars/655262203309719552/ca12b1a43ea265c81535b83fb4d6fb21.webp?size=1024")
        await ctx.send(embed=embed)
        embed.set_footer()

    @commands.command()
    @commands.is_owner()
    @Checks.is_dev()
    async def activity(self, ctx, *, text):
        '''Sets the bots status
        Set the bot's playing status
        activity <Status Text>
        Bot Owner only'''
        game = discord.Game(text)
        await ctx.bot.change_presence(status=discord.Status.online, activity=game)
        await ctx.send(':ok_hand: Done.')

    @activity.error
    async def activityerror(self, ctx, error):
        await ctx.send("Command errored.\n{}".format(error))

    @commands.command(name='say')
    @commands.has_permissions(manage_messages=True)
    async def say(self, ctx, *, text):
        '''Make the bot say something
        Self-explanatory
        say <text>
        Manage Messages'''
        await ctx.send(text)

    # Error handler of the say command
    @say.error
    async def sayerror(self, ctx, error):
        await ctx.send(f"Command errored.\n{error}")

    @commands.has_permissions(manage_messages=True)
    @commands.command()
    @Checks.is_dev()
    async def sayembed(self, ctx, body: str, title: str = None, footer: str = None, color: str = discord.Embed.Empty):
        '''Make the bot say something
        Make the bot say something in embeds. \\nColor have to be a rgb integer number(155012074).
        sayembed <body>|[title]|[footer]|[color]
        Manage Messages'''
        if color is not discord.Embed.Empty:
            color = discord.Color.from_rgb(int(color[0] + color[1] + color[2]),
                                           int(color[3] + color[4] + color[5]),
                                           int(color[6] + color[7] + color[8]))
        embed = discord.Embed(title=title, description=body, color=color)
        if footer is not None:
            embed.set_footer(text=footer, icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def info(self, ctx):
        '''Info command
        This command gives you an invite link to the support server, and also gives you a user to send hatemails to.
        info
        Send messages'''
        embed = discord.Embed(title='Info', description="Hello and welcome to the info section.")
        embed.add_field(name="Support server", value="https://discord.gg/ATCjdFA")
        embed.add_field(name="Hate mails", value="DM <@397029587965575170> or email kcomain@protonmail.com")
        await ctx.send()

    @commands.command(name="help", aliases=['h'])
    async def help(self, ctx, command: str = None):
        '''Help command
        This command only include available extensions/cogs/categories, and in-depth explanations of the specified command.
        help [command name]
        Send messages'''
        if command is None:
            cognames = []
            for i in ctx.bot.commands:
                if i.cog_name not in cognames:
                    cognames.append(i.cog_name)
            out = "`"
            for i in cognames:
                out += f"{i}\n"
            out += "`"
            embed = discord.Embed(title="Waterbot Help",
                                  description='Use .cmds <category name>` to get the available commands in a category',
                                  colour=0xfffbb)
            embed.add_field(name="Available modules of waterbot", value=out)
            embed.set_footer(text="Remove `<>` and `[]`s when using a command.")
            return await ctx.send(embed=embed)
        else:
            stat = 0
            result = None
            for i in ctx.bot.commands:
                if i.name == command:
                    # print('Searching command {command} in commands list (C: {})')
                    stat = 1
                    result = i
                    break
            if stat == 0:
                return await ctx.send(embed=discord.Embed(
                    description=f"No such command. ({command}) \nUse `.help` to list all available modules and use `.cmds <module name>` to check the available commands in that module.",
                    colour=0xff5555))
            else:
                doc = result.help.splitlines()
                embed = discord.Embed(title=f"Help for command `{command}`", colour=0xa12ba1,
                                      timestamp=ctx.message.created_at)
                embed.add_field(name="Short Description", value=doc[0], inline=False)
                embed.add_field(name="Usage", value=ctx.bot.command_prefix + doc[2], inline=False)
                embed.add_field(name="Description", value=re.sub('\\\\n', '\n', doc[1]), inline=False)
                embed.add_field(name="Command Checks", value=doc[3], inline=False)
            await ctx.send(embed=embed)

    @commands.command(name="cmds")
    async def cmds(self, ctx, cogr=None):
        '''List commands available in an extension
        List all commands in an extension/category
        cmds <category name>
        Send messages'''
        # Grab the command list
        try:
            cogr = cogr.capitalize()
        except:
            pass
        cmds = {}
        excluded = [
            'reload'
        ]
        for i in ctx.bot.commands:
            if i.name not in excluded:
                # print(f"Loading command {i}")
                if i.cog_name not in cmds:
                    cmds[i.cog_name] = []
                    cmds[i.cog_name + '_des'] = i.cog.description
                cmds[i.cog_name].append(ctx.bot.command_prefix + i.name)
        if cogr not in cmds:
            return await ctx.send(embed=discord.Embed(description=f"No such category({cogr}).", colour=0xff5555))
        else:
            await ctx.send("Loading", delete_after=5)
        out = "`"
        for i in cmds[cogr]:
            out += f"{i}\n"
        embed = discord.Embed(title=f"Commands in category `{cogr}`", colour=0xa12ba1)
        embed.add_field(name="Category description", value=f"`{cmds[cogr + '_des'].splitlines()[0]}`", inline=False)
        embed.add_field(name="Available commands", value=f"{out}`", inline=False)
        return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Core(bot))
