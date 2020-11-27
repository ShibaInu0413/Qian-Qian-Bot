from discord import Embed, Member, File
from discord.ext import commands

from Core import MongoDB, Cog_Extension
from Core import human_format, nums, LVLKey

from io import BytesIO
from random import choice
from pytz import timezone
from asyncio import sleep
from datetime import datetime
from pymongo import DESCENDING
from requests import get as rget
from PIL import Image, ImageDraw, ImageFont

class LVLCmds(Cog_Extension):
    @commands.command()
    @commands.guild_only()
    @LVLKey()
    async def daily(self, ctx):
        tz = timezone('Asia/Taipei')
        db = MongoDB['level'][str(ctx.guild.id)]
        member = db.find_one({'_id': str(ctx.author.id)})
        if int(datetime.now(tz).strftime('%Y%m%d')) - int(member['daily']) >= 1:
            db.update_one({'_id': str(ctx.author.id)}, {'$set': {'daily': str(datetime.now(tz).strftime('%Y%m%d'))}})
            db.update_one({'_id': str(ctx.author.id)}, {'$set': {'money': str(int(member["money"])+500)}})
            await ctx.send('已領取500銀幣')
        else:
            await ctx.send('時間還沒到喔')

    @commands.command()
    @commands.guild_only()
    @LVLKey()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def filp(self, ctx, ht, num:int):
        db = MongoDB['level'][str(ctx.guild.id)]
        member = db.find_one({'_id': str(ctx.author.id)})
        if int(member['money']) >= num:
            x = ['heads', 'tails']
            if ht in x:
                if num >= 500:
                    msg = await ctx.send('硬幣翻轉中...')
                    xx = choice(x)
                    if ht == xx:
                        db.update_one({'_id': str(ctx.author.id)}, {'$set': {'money': str(int(member["money"])+num)}})
                        await sleep(5)
                        await msg.edit(content='恭喜你猜對了 獲得{}'.format(num))
                    elif ht != xx:
                        db.update_one({'_id': str(ctx.author.id)}, {'$set': {'money': str(int(member["money"])-num)}})
                        await sleep(5)
                        await msg.edit(content='你猜錯囉')
                else:
                    await ctx.send('要大於500喔')
            else:
                await ctx.send('請輸入heads或tails')
        else:
            await ctx.send('你沒這麼多錢喔')

    @commands.command()
    @commands.guild_only()
    @LVLKey()
    async def levels(self, ctx):
        data = list(MongoDB['level'][str(ctx.guild.id)].find().sort([('level', DESCENDING), ('xp', DESCENDING)]))
        text = []
        for i in range(10):
            text.append(f'#{i+1} | <@{int(data[i]["_id"])}> LVL: {data[i]["level"]} XP: {data[i]["xp"]}\n')
        text[0] = "**" + text[0] + "**"
        num = data.index([i for i in data if i["_id"] == str(ctx.author.id)][0])
        levels = Embed(title="此伺服器的等級排行", color=0x00ff40, description="".join(text)).set_footer(text="你的排名: {}".format(num+1), icon_url=ctx.author.avatar_url)
        await ctx.send(embed=levels)

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def setlevel(self, ctx, yn: str):
        if yn == 'yes':
            db = MongoDB['guild'][str(ctx.guild.id)]
            db.update_one({'_id': 'set'}, {'$set': {'level': 'yes'}})
            post = {'_id': 'levelrole'}
            db.insert_one(post)
            await ctx.send('level set to {}'.format(yn))
        elif yn == 'no':
            db = MongoDB['guild'][str(ctx.guild.id)]
            db.update_one({'_id': 'set'}, {'$set': {'level': 'no'}})
            roles = db.find_one({'_id': 'levelrole'})
            if roles != None:
                db.delete_one({'_id': 'levelrole'})
        else:
            await ctx.send('請輸入``yse`` or ``no``')

    @commands.command()
    @commands.guild_only()
    @LVLKey()
    async def rank(self, ctx, member: Member=None):
        await ctx.trigger_typing()
        if member is None:
            author = ctx.author
        elif member is not None:
            author = member
        db = MongoDB['level'][str(ctx.guild.id)].find_one({'_id': str(author.id)})
        if db == None:
            await ctx.send('查詢失敗 : 尚未建立等級卡 聊天後就有囉')
        if db != None:
            avatar_url = rget(author.avatar_url)
            avatar_io = BytesIO(avatar_url.content)
            avatar_a = Image.open(avatar_io).resize((192, 192), Image.ANTIALIAS)
            size = avatar_a.size
            r2 = min(size[0], size[1])
            avatar = Image.new('RGB', (r2, r2),(35 ,39, 42))
            (pima, pimb) = (avatar_a.load(), avatar.load())
            for i in range(r2):
                for j in range(r2):
                    if pow(abs(i - float(r2/2) + 0.5), 2) + pow(abs(j - float(r2/2) + 0.5), 2) <= pow(float(r2/2), 2):
                        pimb[i, j] = pima[i, j]
            num = int(db['xp'])/int((int(db['level'])+1)**4)
            image = Image.open('level/background.png')    
            drawObject = ImageDraw.Draw(image)
            drawObject.ellipse((256+600,182,256+40+600,182+40),fill=(72,75,78))    
            drawObject.ellipse((256,182,256+40,182+40),fill=(72,75,78))    
            drawObject.rectangle((256+(40/2),182, 256+600+(40/2), 182+40),fill=(72,75,78))
            if(num<=0):        
                num = 0.01    
            if(num>1):        
                num=1    
            w = 600*num
            drawObject.ellipse((256+w,182,256+40+w,182+40),fill=(123,175,221))    
            drawObject.ellipse((256,182,256+40,182+40),fill=(123,175,221))    
            drawObject.rectangle((256+(40/2),182, 256+w+(40/2), 182+40),fill=(123,175,221))
            image.paste(avatar, (45, 45))
            drawObject.multiline_text((275, 123), str(author.name), fill=(246, 246, 246), font=ImageFont.truetype('level/華康兒風體W4_1.ttc', size=45))
            drawObject.multiline_text((380, 57), 'RANK', fill=(246, 246, 246), font=ImageFont.truetype('level/華康兒風體W4_1.ttc', size=27))
            drawObject.multiline_text((440, 35), '#' + str(nums(ctx, author)+1), fill=(246, 246, 246), font=ImageFont.truetype('level/華康兒風體W4_1.ttc', size=55))
            drawObject.multiline_text((540, 57), 'LeveL', fill=(123, 175, 221), font=ImageFont.truetype('level/華康兒風體W4_1.ttc', size=27))
            drawObject.multiline_text((610, 35), str(db['level']), fill=(123, 175, 221), font=ImageFont.truetype('level/華康兒風體W4_1.ttc', size=55))
            drawObject.multiline_text((685, 57), 'MONEY', fill=(123, 175, 221), font=ImageFont.truetype('level/華康兒風體W4_1.ttc', size=27))
            drawObject.multiline_text((755, 45), str(human_format(int(db['money']))), fill=(123, 175, 221), font=ImageFont.truetype('level/華康兒風體W4_1.ttc', size=45))
            xp = drawObject.textsize(str(human_format(int(db['xp']))) + '/' + str(human_format((int(db['level'])+1)**4)) + 'XP', font=ImageFont.truetype('level/華康兒風體W4_1.ttc', size=35))
            drawObject.multiline_text((934-xp[1]-175, 140), str(human_format(int(db['xp']))) + '/' + str(human_format((int(db['level'])+1)**4)) + 'XP', fill=(246, 246, 246), font=ImageFont.truetype('level/華康兒風體W4_1.ttc', size=35))
            image.save('level/rank.png')
            await ctx.send(file=File('level/rank.png'))

def setup(client):
    client.add_cog(LVLCmds(client))