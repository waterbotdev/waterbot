import discord
from discord.ext import commands


class AutoRespond(commands.Cog):
    """Autorespond cog, can be disabled"""
    def __init__(self, bot):
        self.bot = bot


class EventResponders(commands.Cog):
    """The cog responsible for event handlers.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        for i in guildconf:
            if member.guild.id == int(i):
                if 'joinchannel' in guildconf[i]:
                    if guildconf[i]['joinchannel'] is not None:
                        channel = bot.get_channel(guildconf[i]['joinlogs']['joinchannel'])
                        try:
                            embed = discord.Embed(title='Welcome new member!',
                                                  description=f'Welcome **{member.name}** to **{member.guild.name}**.\n'
                                                              f'There are now **{len(member.guild.members)}** members.',
                                                  color=0xffffff)
                            await channel.send(embed=embed)
                        except Exception as e:
                            await bot.get_channel(668447749443813416).send(f'Error in event on_member_join'
                                                                           f'Server: {member.guild.name}({member.guild.id})'
                                                                           f'Messag: {e}')

    @commands.Cog.listener()
    async def on_member_remove(member):
        for i in guildconf:
            if member.guild.id == int(i):
                if 'leavechannel' in guildconf[i]:
                    if guildconf[i]['leavechannel'] is not None:
                        channel = bot.get_channel(guildconf[i]['joinlogs']['leavechannel'])
                        try:
                            embed = discord.Embed(title='Goodbye',
                                                  description=f'Bye bye **{member.name}**.\n'
                                                              f'There are now **{len(member.guild.members)}** members.',
                                                  color=0xaaaaaa)
                            await channel.send(embed=embed)
                        except Exception as e:
                            await bot.get_channel(668447749443813416).send(f'Error in event on_member_leave'
                                                                           f'Server : {member.guild.name}({member.guild.id})'
                                                                           f'Message: {e}')


def setup(bot):
    bot.add_cog(AutoRespond(bot))
    bot.add_cog(EventResponders(bot))
