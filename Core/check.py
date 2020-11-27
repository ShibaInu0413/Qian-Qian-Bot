from discord.ext import commands

from .LoadDumpFile import MongoDB

from pymongo import DESCENDING

class LevelError(commands.CommandError): pass

def LVLKey():
    def predicate(ctx):
        guilds = MongoDB['guild'][str(ctx.guild.id)].find_one({"_id": "set"})
        if guilds['level'] == 'yes': return True
        elif guilds['level'] != 'yes': raise LevelError
    return commands.check(predicate)

def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

def nums(ctx, author):
    data = list(MongoDB['level'][str(ctx.guild.id)].find().sort([('level', DESCENDING), ('xp', DESCENDING)]))
    num = 0
    for i in data:
        if i["_id"] != str(author.id): num += 1
        elif i["_id"] == str(author.id): break
    return num