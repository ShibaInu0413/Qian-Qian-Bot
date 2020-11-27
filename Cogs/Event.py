from discord import Embed, GroupChannel, DMChannel
from discord.ext import commands

from Core import Cog_Extension, LevelError, MongoDB

from datetime import datetime

class Event(Cog_Extension):
    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        if ctx.author != self.client.user:
            command = Embed(title="指令日誌 | Command Log", color=0x00ff40, timestamp=datetime.now())
            if not isinstance(ctx.channel, (GroupChannel, DMChannel)):
                command.add_field(name="伺服器 | Guild", value=f'`{ctx.guild.name}`', inline=True)
                command.add_field(name="頻道 | Channel", value=f'{ctx.channel.mention}', inline=True)
            command.add_field(name="使用者 | User", value=f'{ctx.author.mention}', inline=True)
            command.add_field(name="訊息 | Message", value=f'`{ctx.message.content}`', inline=True)
            await self.client.get_channel(677746786420391956).send(embed=command)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send('無效的指令 O.o')
        elif isinstance(error, commands.BadArgument):
            pass
        elif isinstance(error, commands.NotOwner):
            await ctx.send('你不是主人 O.o')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send('權限不足 O.o')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'缺少引數 O.o')
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'冷卻時間剩{int(error.retry_after)}秒')
        elif isinstance(error, commands.NSFWChannelRequired):
            await ctx.send('此頻道無nsfw標籤')
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send('此指令無法再私訊中使用')
        elif isinstance(error, LevelError):
            pass
        else:
            ErrorInfo = Embed(title="錯誤 | Error", color=0x00ff40, timestamp=datetime.now())
            if not isinstance(ctx.channel, (GroupChannel, DMChannel)):
                ErrorInfo.add_field(name="伺服器 | Guild", value=f'`{ctx.guild.name}`', inline=True)
                ErrorInfo.add_field(name="頻道 | Channel", value=f'{ctx.channel.mention}', inline=True)
            ErrorInfo.add_field(name="使用者 |User", value=f'{ctx.author.mention}', inline=True)
            ErrorInfo.add_field(name="錯誤 | Error", value=f'`{error}`', inline=True)
            await self.client.get_channel(677123064126898187).send(embed=ErrorInfo)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        db = MongoDB['guild'][str(guild.id)]
        post = {'_id': 'set', 'level': 'no'}
        db.insert_one(post)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await self.client.get_channel(720798027828166747).send(f'<@!498476320960020491> 已退出``{guild.name}``\nID: ``{guild.id}``')

    @commands.Cog.listener()
    async def on_message(self, msg):
        if isinstance(msg.channel, (GroupChannel, DMChannel)) and msg.author != self.client.user:
            dm_message = Embed(title='芊芊醬的私人消息', description="**私訊者**:{}({})\n**訊息**:\n{}".format(msg.author.mention, msg.author.id, msg.content), color=0x00ff40)
            dm_message.set_author(name=f'{msg.author.name}', icon_url=msg.author.avatar_url)
            await self.client.get_channel(678266850261598248).send(embed=dm_message)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.name == "DCHK":
            await member.guild.ban(member)

def setup(client):
    client.add_cog(Event(client))