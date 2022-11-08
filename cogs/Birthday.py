import discord
from discord import permissions
from discord.ext import commands, tasks
from discord.ext.commands.core import command
import motor.motor_asyncio
from discord import Embed
from datetime import datetime
import pytz

mongoURL = ""
cluster = motor.motor_asyncio.AsyncIOMotorClient(mongoURL)
db = cluster["phoenixDB"]
collection = db["Birthdays"]

class Birthday(commands.Cog):
    def __init__(self, client):
        self.client = client

    def areAllDigits(text):
        for c in text:
            if c.isdigit() == False:
                return False

    @commands.command(aliases=['b'])
    async def birthday(self, ctx, birthday : str):
        user_id = ctx.author.id
        tz_RO = pytz.timezone("Europe/Bucharest")
        datetime_RO = datetime.now(tz_RO)
        luna = str(datetime_RO.strftime('%m'))
        zi = str(datetime_RO.strftime('%d'))
        if len(zi) == 1:
            zi = f"0{zi}"
        birthday_d = birthday[0:2]
        birthday_m = birthday[3:5]
        if birthday == None:
            await ctx.send(f'**Comanda este: `ph?birthday zz/ll`**')
            return
        if zi == birthday_d and luna == birthday_m:
            await ctx.send(f"**Nu poti sa iti alegi data actuala.**")
            return
        if Birthday.areAllDigits(birthday_d) == False or Birthday.areAllDigits(birthday_m) == False:
            await ctx.send(f'**Ai gresit formatul. `zz/ll`**')
            return
        if int(birthday_d) > 31 or int(birthday_m) > 12:
            await ctx.send(f'**Data nu exista.**')
            return
        birthday_format = f"{birthday_d}/{birthday_m}"
        if await collection.count_documents({"_id":user_id}) == 0: # Daca nu se afla in Birthdays
            await collection.insert_one({"_id":user_id})
            await collection.update_one({"_id":user_id}, {"$set":{"birthday":birthday_format}}, upsert = True)
            await ctx.send(f"**Ti-ai setat ziua de nastere :** `{birthday_format}`")
        else: # Se afla in Birthdays
            await ctx.send(f"**Ca sa iti editezi ziua de nastere, contacteaza un membru STAFF.**")

    @commands.command(aliases=['cb'])
    @commands.has_role(876759046336688138)
    async def changebirthday(self, ctx, member : discord.Member, birthday : str):
        user_id = member.id
        birthday_d = birthday[0:2]
        birthday_m = birthday[3:5]
        tz_RO = pytz.timezone("Europe/Bucharest")
        datetime_RO = datetime.now(tz_RO)
        luna = str(datetime_RO.strftime('%m'))
        zi = str(datetime_RO.strftime('%d'))
        if len(zi) == 1:
            zi = f"0{zi}"
        if zi == birthday_d and luna == birthday_m:
            await ctx.send(f"**Nu poti schimba cu data actuala. (Ziua membrului)**")
            return

        user_id = member.id
        if birthday == None or member == None:
            await ctx.send(f'**Comanda este: `ph?changebirthday <membru> zz/ll`**')
            return
        if Birthday.areAllDigits(birthday_d) == False or Birthday.areAllDigits(birthday_m) == False:
            await ctx.send(f'**Ai gresit formatul. `zz/ll`**')
            return
        if int(birthday_d) > 31 or int(birthday_m) > 12:
            await ctx.send(f'**Data nu exista.**')
            return
        birthday_format = f"{birthday_d}/{birthday_m}"
        if await collection.count_documents({"_id":user_id}) == 0:
            await ctx.send("**Membrul specificat nu si-a setat ziua de nastere.**")
            return
        else:
            await collection.update_one({"_id":user_id}, {"$set":{"birthday":birthday_format}}, upsert = True)
            await ctx.send(f"**Ai setat ziua de nastere a membrului {member.mention} :** `{birthday_format}`")

    @tasks.loop(minutes = 45)
    async def birthdays(self):
        tz_RO = pytz.timezone("Europe/Bucharest")
        datetime_RO = datetime.now(tz_RO)

        luna = str(datetime_RO.strftime('%m'))
        zi = str(datetime_RO.strftime('%d'))
        if len(zi) == 1:
            zi = f"0{zi}"
        ora = int(datetime_RO.strftime('%H'))
        #minute = int(datetime_RO.strftime('%M'))
        result = collection.find()
        # Cautam in baza de birthday
        async for i in result:#
            i_bd = i["birthday"]
            i_id = i["_id"]
            birthday_d = i_bd[0:2]
            birthday_m = i_bd[3:5]
            channel = self.client.get_channel(570305206139748353)
            gui = self.client.get_guild(569077625826443274)
            person = gui.get_member(i_id)
            if(zi == birthday_d and luna == birthday_m and ora == 0):
                if await collection.count_documents({"_id":i_id, "birthdaycheck":{"$exists":True}}) == 0:
                    # Nu exista checkul
                    await collection.update_one({"_id":i_id}, {"$set":{"birthdaycheck":0}}, upsert = True)
                    # Bagam checkul
                    title = f":birthday: LA MULTI ANI! :birthday:"
                    description = f"""
                        <:line:844914054095175680><:line:844914054095175680><:line:844914054095175680><:line:844914054095175680><:line:844914054095175680><:line:844914054095175680><:line:844914054095175680><:line:844914054095175680><:line:844914054095175680><:line:844914054095175680><:line:844914054095175680><:line:844914054095175680><:line:844914054095175680><:line:844914054095175680><:line:844914054095175680><:line:844914054095175680> \n
                        **Azi este ziua de nastere a membrului** {person.mention} **!** <:heartyy:844922846715314176>
                        <:stary:844988233691693076> **Haideti sa ii uram un "La multi ani!"** \n
                        <:line:844914054095175680><:line:844914054095175680><:line:844914054095175680><:line:844914054095175680><:line:844914054095175680><:line:844914054095175680><:line:844914054095175680><:line:844914054095175680><:line:844914054095175680><:line:844914054095175680><:line:844914054095175680><:line:844914054095175680><:line:844914054095175680><:line:844914054095175680><:line:844914054095175680><:line:844914054095175680>
                    """
                    embed_1 = Embed(color = 0xffb20c, title = title, description = description, timestamp = datetime.utcnow().strftime('%d/%m/%y'))
                    embed_1.set_author(name = f'{person.display_name}#{person.discriminator}', icon_url = person.avatar_url)
                    embed_1.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/768118506813390859/845180151586095104/download_4.png')
                    embed_1.set_footer(text = 'La multi ani!', icon_url = 'https://cdn.discordapp.com/attachments/842428676439539722/844988370572804146/gasdh.png')
                    await channel.send(embed = embed_1)
            if(zi == birthday_d and luna == birthday_m and ora == 23):
                await collection.update_one({"_id":i_id}, {"$unset":{"birthdaycheck":0}}, upsert = True)
                # Scoatem checkul
                channel = self.client.get_channel(570305206139748353)
                embed_2 = Embed(color = 0x0d0822, description = f'**Ziua ta de nastere a trecut,** {person.mention}**...** <:whyudothis:836918665604890625>', timestamp = datetime.utcnow())
                await channel.send(embed = embed_2)

    @commands.Cog.listener()
    async def on_ready(self):
        self.birthdays.start()

def setup(client):
    client.add_cog(Birthday(client))
