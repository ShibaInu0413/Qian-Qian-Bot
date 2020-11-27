from discord.utils import get
from discord import User, Member
from discord.ext import commands

from Core import Cog_Extension

from asyncio import sleep

class Admin(Cog_Extension):
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member: User, *,reason=None):
        await ctx.guild.kick(member, reason=reason)
        await ctx.send(f'kicked {member.mention}\nreason:{reason}')

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, user: User, *,reason=None):
        await ctx.guild.ban(user, reason=reason, delete_message_days=7)
        await ctx.send(f'Banned {user.mention}\nreason:{reason}')

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, *, member: int):
        banned_users = await ctx.guild.bans()
        for ban_entry in banned_users:
            user = ban_entry.user
            if user.id == member:
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.mention}')

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx, member: Member):
        role = get(ctx.guild.roles, name='Muted')
        if role == None:
            role = await ctx.guild.create_role(name='Muted')
        await member.add_roles(role)
        await ctx.send(f'**{member.mention}**已被禁言')
        for channel in ctx.guild.channels:
            await channel.set_permissions(role, send_messages=False)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def unmute(self, ctx, member: Member):
        role = get(ctx.guild.roles, name='Muted')
        if role != None:
            await member.remove_roles(role)
            await ctx.send(f'**{member.mention}**已解除禁言')

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True) 
    async def clear(self, ctx: commands.Context, num: int):
        await ctx.channel.purge(limit=num+1)
        await ctx.send(f'已刪除{num}則訊息', delete_after=5.0)

def setup(client):
    client.add_cog(Admin(client))