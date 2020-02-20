import io
import json
import asyncio
import discord
import inspect
import aiohttp
import textwrap
import traceback
# import inspect
import subprocess

from contextlib import redirect_stdout

from .helpers.util import cleanup_code, get_syntax_error
from discord.ext import commands

botConfig = json.load(open('configs/config.json'))


# Certain code fragments below is written by Rapptz.
# Said commands will have the `# AUTHOR: RAPPTZ` comment
# before the definition of the command.


class Dev(commands.Cog):
    '''Developer commands'''

    def __init__(self, bot):
        self.bot = bot
        self._last_result = None
        self.sessions = set()

    async def cog_check(self, ctx):
        return ctx.author.id in botConfig['developers']

    @commands.command(name='die', aliases=['disconnect'])
    async def die(self, ctx):
        '''Kills the bot
        Kills the bot
        die
        Developers only'''
        await ctx.send(
            f'<:angrysponge:668767678273683474> You\'ve made a big fault, {ctx.author.mention}. '
            f'The bell of awakening is coming soon for you..')
        await ctx.bot.close()

    @commands.command(name='gitpull', aliases=['gpull', 'pull'])
    async def gitpull(self, ctx):
        '''Update local repo
        Updates local code repo from github.
        [gitpull|gpull|pull]
        Developers only'''
        msg = await ctx.send(embed=discord.Embed(title='Updating...', description='Initializing...'))
        await asyncio.sleep(1)
        await msg.edit(
            embed=discord.Embed(title='Running `git fetch`...', description='Waiting for logs...', color=0xf7eb60))
        run = subprocess.run(['git', 'fetch'], stdout=subprocess.PIPE)
        await msg.edit(
            embed=discord.Embed(title='Running git fetch...', description=f'```{"No Logs."}```', color=0xf7eb60))
        await asyncio.sleep(3)
        await msg.edit(
            embed=discord.Embed(title='Running `git merge`...', description='Waiting for logs...', color=0xf7eb60))
        run = subprocess.run(['git', 'merge'], stdout=subprocess.PIPE)
        await msg.edit(
            embed=discord.Embed(title='Running `git merge`...', description=f'```py\n{run.stdout.decode()}```',
                                color=0xf7eb60))
        await asyncio.sleep(3)
        await msg.edit(
            embed=discord.Embed(title='Running `starter.bat`...', description='Restarting...', color=0x31d90b))
        run = subprocess.run(['cmd', '/K', 'starter.bat'])
        await msg.edit(embed=None, content='Restarting...')
        await ctx.bot.logout()

    @commands.command(name='announce')
    async def announce(self, ctx, size: str, title: str, *, details: str):
        '''Announce something
        Announce bot updates in the channel.
        announce <s|b> <title> <details>
        Developers only.'''
        if size == "s":
            channel = ctx.bot.get_channel(botConfig['minornews'])
            color = 0xf5d442
        elif size == "b":
            channel = ctx.bot.get_channel(botConfig['majornews'])
            color = 0xf7401b
        else:
            return await ctx.send('Invalid size. It have to be `s`(small/minor) or `b`(big/major).')
        await ctx.message.delete()
        embed = discord.Embed(color=color, title=title, description=details, timestamp=ctx.message.created_at)
        embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await channel.send(embed=embed)

    @commands.command()
    async def fjaosfhuaihfus89679y(self, ctx, count: int = 20):
        messages = []
        for i in range(count):
            msg = await ctx.send('<@513603936033177620>')
            messages.append(msg)
        for i in messages:
            await i.delete()

    @commands.command()
    async def status(self, ctx, stat: str, text: str = None):
        '''Change the overall status of the bot
        The command have 3 different modes: operational(online), temporary outage(idle) and Severe outage(dnd)
        status <online|idle|dnd>
        Developers only'''
        if stat == 'online':
            if text is not None:
                f = open('configs/config.json')
                que = json.load(f)
                que['status'] = text
                f.close()
                f = open('configs/config.json', 'w')
                json.dump(que, f)
                f.close()
                return await self.bot.change_presence(status='online', activity=discord.Game(name=text))
            else:
                return await ctx.send('U wot? missing text parameter.')
        elif stat == 'idle':
            if text is None:
                text = "Temporary Outage."
                return await self.bot.change_presence(status='online', activity=discord.Game(name=text))
            else:
                return await self.bot.change_presence(status='idle',
                                                      activity=discord.Game(name=f'Temporary Outage|{text}'))
        elif stat == 'dnd':
            return await self.bot.change_presence(
                status='dnd',
                activity=discord.Game(
                    name='Major outage' if text is not None else f'Outage: {text}'))

    # AUTHOR: RAPPTZ
    @commands.command()
    async def _eval(self, ctx, *, code: str):
        '''Eval code
        Evaluate code.
        eval <code object>
        Developers only'''
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'guild': ctx.guild,
            'author': ctx.author,
            'msg': ctx.message
        }
        env.update(globals())
        code = cleanup_code(code)
        stdout = io.StringIO()
        to_cmp = f'async def __f():\n{textwrap.indent(code, "   ")}'
        try:
            exec(to_cmp, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e}\n```')

        func = env["func"]
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2714')
            except:
                pass

        if ret is None:
            if value:
                await ctx.send(f'```py\n{value}\n```')
        else:
            await ctx.send(f'```py\n{value}{ret}\n```')

    # AUTHOR: RAPPTZ
    @commands.command(pass_context=True, hidden=True)
    async def repl(self, ctx):
        """Launches an interactive REPL session."""
        variables = {
            'ctx': ctx,
            'bot': self.bot,
            'message': ctx.message,
            'guild': ctx.guild,
            'channel': ctx.channel,
            'author': ctx.author,
            '_': None,
        }

        if ctx.channel.id in self.sessions:
            await ctx.send('Already running a REPL session in this channel. Exit it with `quit`.')
            return

        self.sessions.add(ctx.channel.id)
        await ctx.send('Enter code to execute or evaluate. `exit()` or `quit` to exit.')

        def check(m):
            return m.author.id == ctx.author.id and \
                   m.channel.id == ctx.channel.id and \
                   m.content.startswith('`')

        while True:
            try:
                response = await self.bot.wait_for('message', check=check, timeout=10.0 * 60.0)
            except asyncio.TimeoutError:
                await ctx.send('Exiting REPL session.')
                self.sessions.remove(ctx.channel.id)
                break

            cleaned = cleanup_code(response.content)

            if cleaned in ('quit', 'exit', 'exit()'):
                await ctx.send('Exiting.')
                self.sessions.remove(ctx.channel.id)
                return

            executor = exec
            if cleaned.count('\n') == 0:
                # single statement, potentially 'eval'
                try:
                    code = compile(cleaned, '<repl session>', 'eval')
                except SyntaxError:
                    pass
                else:
                    executor = eval

            if executor is exec:
                try:
                    code = compile(cleaned, '<repl session>', 'exec')
                except SyntaxError as e:
                    await ctx.send(get_syntax_error(e))
                    continue

            variables['message'] = response

            fmt = None
            stdout = io.StringIO()

            try:
                with redirect_stdout(stdout):
                    result = executor(code, variables)
                    if inspect.isawaitable(result):
                        result = await result
            except Exception as e:
                value = stdout.getvalue()
                fmt = f'```py\n{value}{traceback.format_exc()}\n```'
            else:
                value = stdout.getvalue()
                if result is not None:
                    fmt = f'```py\n{value}{result}\n```'
                    variables['_'] = result
                elif value:
                    fmt = f'```py\n{value}\n```'

            try:
                if fmt is not None:
                    if len(fmt) > 2000:
                        await ctx.send('Content too big to be printed.')
                    else:
                        await ctx.send(fmt)
            except discord.Forbidden:
                pass
            except discord.HTTPException as e:
                await ctx.send(f'Unexpected error: `{e}`')

    @commands.group(invoke_without_command=True)
    async def botset(self, ctx):
        '''Set the bot's different attributes
        This command is a group, that means you have to use a subcommand in order to change anything.\\nIf you run this command once, you'll be getting all the subcommands available.
        botset [subcommand] [<setting>]
        Developers only'''
        desc = ""
        desc += "`botset username`: change the username for the bot\n"
        desc += "`botset pfp`: change the bot's profile picture to the one thee url spefcified\n"
        # desc += "`botset <subcommand>`: \n"
        embed = discord.Embed(title='Subcommands for `botset`', description=desc)
        await ctx.send(embed=embed)

    @botset.command()
    async def username(self, ctx, name: str = None):
        '''Change the username
        Change the username for the bot.
        botset username <name>'''
        oldname = ctx.bot.user.name
        if name is None:
            return await ctx.send('Give me a name to change man')
        await ctx.bot.user.edit(username=name)
        await ctx.send(f'Changed username from {oldname} to {name}.')

    @botset.command()
    async def pfp(self, ctx, url: str = None):
        '''Change the pfp of the bot user
        Changes the bot user's profile picture to the one specified in the url parameter/the image attached.
        botset pfp <image url/attach photo>
        Developers only'''
        if url is None:
            try:
                url = ctx.message.attachments[0]
            except IndexError:
                return await ctx.send('You did not give me any image whatsoever.')

        async with aiohttp.ClientSession() as session:
            r = await session.get(url=url)
            data = await r.read()
            await ctx.bot.user.edit(avatar=data)
            r.close()
        await ctx.send('Changed pfp!')


def setup(bot):
    bot.add_cog(Dev(bot))
