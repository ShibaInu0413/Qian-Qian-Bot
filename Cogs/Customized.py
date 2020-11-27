from discord.ext import commands
from discord.utils import get as dget

from Core import Cog_Extension

class 女友芊芊的陪聊間(Cog_Extension):
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == 613801330955386895:
            role = dget(member.guild.roles, id=int("718652826661814283"))
            await member.add_roles(role)

class 粉紅色的羽毛堆(Cog_Extension):
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == 602772115636224010:
            role = dget(member.guild.roles, id=int("712710943053709342"))
            await member.add_roles(role)

def setup(client):
    client.add_cog(女友芊芊的陪聊間(client))
    client.add_cog(粉紅色的羽毛堆(client))