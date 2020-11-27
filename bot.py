from discord import Embed, Intents
from discord.ext import commands

from time import time
from datetime import datetime
from os import getenv, listdir

from flask import Flask
from threading import Thread

class Bot(commands.Bot):
    def __init__(self, prefix: str):
        super(Bot, self).__init__(command_prefix=prefix, intents=Intents().all(), help_command=None)
        self.start_time = datetime.utcnow()

    async def on_ready(self):
        print(">>Bot on ready<<")

    @property
    def uptime(self):
        now = datetime.utcnow()
        delta = now - self.start_time

        hours, temainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(temainder, 60)
        day, hours = divmod(hours, 24)

        return f'{day}D {hours}H {minutes}M {seconds}S'

    def _text_channel(self):
        for guild in self.guilds:
            for channel in guild.text_channels:
                yield channel

    def _voice_channel(self):
        for guild in self.guilds:
            for channel in guild.voice_channels:
                yield channel

    def _users(self):
        for user in self.users:
            if not user.bot:
                yield user

    async def _Websocket(self, ctx):
        start = time()
        await ctx.trigger_typing()
        end = time()
        return end - start

app = Flask('')
client = Bot("&")

@client.command()
@commands.is_owner()
async def info(ctx):
    AboutEmbed = Embed(timestamp=datetime.now(), color=0x00ff40)
    AboutEmbed.add_field(name="Stats", value=f"```css\n{len(client.guilds)} servers\n{client.shard_count} shard\n```")
    AboutEmbed.add_field(name="Users", value=f"```css\n{len(list(client._users()))} unique\n{len(client.users)} total\n```")
    AboutEmbed.add_field(name="Channels", value=f"```css\n{len(list(client._text_channel()))} Text\n{len(list(client._voice_channel()))} Voice\n```")
    AboutEmbed.add_field(name="Latency", value=f"```css\n{str(round(client.latency*1000))}ms\n```")
    AboutEmbed.add_field(name="Websocket", value=f"```css\n{str(round(await client._Websocket(ctx)*1000))}ms\n```")
    AboutEmbed.add_field(name="Uptime", value=f"```css\n{client.uptime}```")
    await ctx.send(embed=AboutEmbed)

@client.command()
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f'Cogs.{extension}')
    await ctx.send(f'Load **{extension}** done.')

@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f'Cogs.{extension}')
    await ctx.send(f'UnLoad **{extension}** done.')

@client.command()
@commands.is_owner()
async def reload(ctx, extension):
    client.reload_extension(f'Cogs.{extension}')
    await ctx.send(f'ReLoad **{extension}** done.')

for filename in listdir('./Cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'Cogs.{filename[:-3]}')

@app.route('/')
def main(): return "Bot is aLive!"

def run(): app.run(host="0.0.0.0", port=8080)

def KeepAlive(): Thread(target=run).start()

KeepAlive()
if __name__ == "__main__":
    client.run(getenv("TOKEN"))