from discord import GroupChannel, DMChannel
from discord.ext import commands

from Core import Cog_Extension, MongoDB

from random import randint

async def update_data(db, member, ID):
    if member is None:
        member = {}
        member["_id"] = str(ID)
        member["created_at"] = "0"
        member["level"] = 1
        member["xp"] = 0
        member["money"] = "0"
        member["daily"] = "0"
        db.insert_one(member)
        return member
    return member

async def add_xp(db, member, time, exp):
    if int(time) - int(member['created_at']) >= 100:
        db.update_one({'_id': member["_id"]}, {'$set': {'created_at': str(time)}})
        db.update_one({'_id': member["_id"]}, {'$set': {'money': str(int(member["money"])+randint(5, 15))}})
        db.update_one({"_id": member["_id"]}, {"$set": {"xp": int(member["xp"])+exp}})
        return int(member["xp"]) + exp
    return int(member["xp"])

async def level_up(db, author, level, xp, channel):
    if int(float(level)) < int(float(xp) ** (1/4)):
        db.update_one({"_id": str(author.id)}, {"$set": {"level": int(float(xp) ** (1/4))}})
        # await channel.send(f"<a:emoji_10:693034974936432730> 恭喜{author.mention}等級提升至{int(int(xp) ** (1/4))}")
        return int(float(xp) ** (1/4))
    return int(float(xp) ** (1/4))

class LVLEvent(Cog_Extension):
    @commands.Cog.listener()
    async def on_message(self, msg):
        if not msg.author.bot and not isinstance(msg.channel, (GroupChannel, DMChannel)):
            guild = MongoDB['guild'][str(msg.guild.id)]
            if guild.find_one({"_id": "set"})['level'] == 'yes':
                db = MongoDB['level'][str(msg.guild.id)]
                member = db.find_one({'_id': str(msg.author.id)})

                member = await update_data(db, member, msg.author.id)
                xp = await add_xp(db, member, msg.created_at.strftime('%Y%m%d%H%M%S'), randint(1, 5))
                level = await level_up(db, msg.author, member["level"], xp, msg.channel)

                levelrole = guild.find_one({"_id": "levelrole"})
                if str(level) in levelrole:
                    role = msg.guild.get_role(levelrole[str(level)])
                    if role != None:
                        await msg.guild.get_member(msg.author.id).add_roles(role)

def setup(client):
    client.add_cog(LVLEvent(client))