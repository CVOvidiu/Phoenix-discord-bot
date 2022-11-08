import discord
import asyncio
import motor.motor_asyncio
import datetime
from discord.ext import commands
from discord import Emoji
from discord import Embed, Emoji
from discord.utils import get
from discord.ext.commands import BucketType

mongoURL = ""
cluster = motor.motor_asyncio.AsyncIOMotorClient(mongoURL)
db = cluster["phoenixDB"]
collection = db["phoenixCollection"]

date_today = datetime.date.today()
date_today = str(date_today)

class Marry(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(3, 30, commands.BucketType.user)
    async def divorce(self, ctx):
        global collection
        global db
        global cluster
        global mongoURL
        user_id = ctx.author.id

        i_married = collection.find({"_id":user_id}, {"married":True})
        async for x in i_married:
            gui = self.client.get_guild(id = 569077625826443274)
            x_aux = x["married"]
            i_married_to = gui.get_member(user_id = x_aux)
        await ctx.send(embed = Embed(color=0xff006f, description = f"{ctx.author.mention} **, vrei sa divortezi de** {i_married_to.mention} **? (DA/NU) |** :grey_question:"), delete_after=30)
        try:
            message = await self.client.wait_for("message", check = lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30.0)

        except asyncio.TimeoutError:
            await ctx.send(embed = Embed(color=0xff006f, description = "**Timeout |** :alarm_clock:"), delete_after=20)

        else:
            if message.content.lower() == "da":
                result = collection.find({"_id":user_id}, {"married":True})
                async for i in result:
                    gui = self.client.get_guild(id = 569077625826443274)
                    i_aux = i["married"]
                    married_to = gui.get_member(user_id = i_aux)
                    await collection.update_one({"_id":i_aux}, {"$unset":{"married":1}})
                    await collection.update_one({"_id":user_id}, {"$unset":{"married":1}})
                    await collection.update_one({"_id":user_id}, {"$unset":{"marrytime":1}})
                    await collection.update_one({"_id":i_aux}, {"$unset":{"marrytime":1}})
                    result2 = collection.find({"_id":user_id}, {"_id":1})
                    result3 = collection.find({"_id":user_id})
                    result4 = collection.find({"_id":i_aux}, {"_id":1})
                    result5 = collection.find({"_id":i_aux})
                    async for i4 in result4:
                        async for i5 in result5:
                            if i4 == i5:
                                await collection.delete_one({"_id":i_aux})
                    async for i2 in result2:
                        async for i3 in result3:
                            if i2 == i3:
                                await collection.delete_one({"_id":user_id})
                await ctx.send(embed = Embed(color=0xff006f, description = f"**Tu si** {married_to.mention} **ati divortat! |** :white_check_mark:"), delete_after=20)
            elif message.content.lower() == "nu":
                await ctx.send(embed = Embed(color=0xff006f, description = "**Ai anulat comanda. |** :leftwards_arrow_with_hook:"), delete_after=20)
            else:
                await ctx.send(embed = Embed(color=0xff006f, description = f"**Te rog raspunde cu `DA` sau `NU` la intrebare! Incearca comanda din nou... |** :dizzy_face:"), delete_after=15)

    @commands.command()
    @commands.cooldown(3, 30, commands.BucketType.user)
    async def whomarried(self, ctx, member : discord.Member = None):
        global collection
        global db
        global cluster
        global mongoURL
        user_id = ctx.author.id

        if member == None:
            await ctx.send(embed = Embed(color=0xff006f, description = "**Ceva nu a mers bine! Foloseste :** `ph?whomarried <member>` **|** :no_entry_sign:"), delete_after=20)
        else:
            member_id = member.id
            if await collection.count_documents({"_id":member_id}) == 0: # Membrul nu este in baza
                await ctx.send(embed = Embed(color=0xff006f, description = "**Membrul nu este casatorit.**"), delete_after=20)
            elif await collection.count_documents({"_id":member_id, "married":{"$exists":True}}) == 0: # Membrul este in baza dar nu este married
                await ctx.send(embed = Embed(color=0xff006f, description = "**Membrul nu este casatorit.**"), delete_after=20)
            elif await collection.count_documents({"_id":member_id, "married":{"$exists":True}}) != 0: # Membrul este in baza si este married
                result = collection.find({"_id":member_id}, {"married":True, "marrytime":True})
                async for i in result:
                    gui = self.client.get_guild(id = 569077625826443274)
                    i_aux = i["married"]
                    i_at = i["marrytime"]
                    married_to = gui.get_member(user_id = i_aux)
                    await ctx.send(embed = Embed(color=0xff006f, description = f"{member.mention} **s-a casatorit cu** {married_to.mention} pe data de `{i_at}`**.**"), delete_after=20)

    @commands.command()
    @commands.cooldown(3, 30, commands.BucketType.user)
    async def marry(self, ctx, member : discord.Member = None):
        global collection
        global db
        global cluster
        global mongoURL
        global date_today
        user_id = ctx.author.id


        if member == None: # 'member' nu este specificat
            if await collection.count_documents({"_id":user_id}) == 0: # Numarul documentelor in care apare id-ul userului este 0 (adica nu apare in baza de date)
                await ctx.send(embed = Embed(color=0xff006f, description = "**Nu esti casatorit!**"), delete_after=20)
            else: # Userul este in baza de date
                if await collection.count_documents({"_id":user_id, "married":{"$exists":True}}) == 0: # Daca nu exista fieldul 'married'
                    await ctx.send(embed = Embed(color=0xff006f, description = "**Nu esti casatorit!**"), delete_after=20)
                else: # Daca exista fieldul 'married'
                    result2 = collection.find({"_id":user_id}, {"married":True, "marrytime":True}) # Cauta si returneaza documentul cu id + married
                    async for i2 in result2:
                        gui = self.client.get_guild(id = 569077625826443274)
                        i_aux = i2["married"]
                        i_at = i2["marrytime"]
                        married_to = gui.get_member(user_id = i_aux)
                        await ctx.send(embed = Embed(color=0xff006f, description = f"**Tu si {married_to.mention} sunteti casatoriti din data de `{i_at}`.**"), delete_after=20)
        elif member == ctx.author:
            await ctx.send(embed = Embed(color=0xff006f, description = "**Nu poti face asta! |** :no_entry_sign:"), delete_after=20)
        else: # Daca membrul este specificat
            member_id = member.id

            if await collection.count_documents({"_id":user_id}) == 0: # Userul nu este in baza
                
                if await collection.count_documents({"_id":member_id}) == 0: # Membrul nu este in baza
                    await ctx.send(embed = Embed(color=0xff006f, description = f"{ctx.author.mention} **, vrei sa te casatoresti cu** {member.mention} **? (DA/NU)**"), delete_after=30)

                    try:
                        message = await self.client.wait_for("message", check = lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30.0)

                    except asyncio.TimeoutError:
                        await ctx.send(embed = Embed(color=0xff006f, description = "**Timeout |** :alarm_clock:"), delete_after=20)

                    else:
                        if message.content.lower() == "da":
                            await ctx.send(embed = Embed(color=0xff006f, description = f"{member.mention} **, vrei sa te casatoresti cu** {ctx.author.mention} **? (DA/NU)**"), delete_after=30)

                            try:
                                message2 = await self.client.wait_for("message", check = lambda m: m.author == member and m.channel == ctx.channel, timeout=30.0)
                            
                            except asyncio.TimeoutError:
                                    await ctx.send(embed = Embed(color=0xff006f, description = "**Timeout |** :alarm_clock:"), delete_after=20)

                            else:
                                if message2.content.lower() == "da":
                                    await collection.insert_one({"_id":user_id}) # Introdu id-ul userului in baza
                                    await collection.update_one({"_id":user_id}, {"$set":{"married":member_id}}, upsert=True)
                                    await collection.insert_one({"_id":member_id}) # Introdu id-ul membrului in baza
                                    await collection.update_one({"_id":member_id}, {"$set":{"married":user_id}}, upsert=True)
                                    await collection.update_one({"_id":user_id}, {"$set":{"marrytime":date_today}})
                                    await collection.update_one({"_id":member_id}, {"$set":{"marrytime":date_today}})
                                    await ctx.send(embed = Embed(color=0xff006f, description = f"{ctx.author.mention} **si** {member.mention} **s-au casatorit!**"))
                                elif message2.content.lower() == "nu":
                                    await ctx.send(embed = Embed(color=0xff006f, description = "**Ai refuzat cererea in casatorie! |** :scream:"))
                                else:
                                    await ctx.send(embed = Embed(color=0xff006f, description = f"**Te rog raspunde cu `DA` sau `NU` la intrebare! Incearca comanda din nou... |** :dizzy_face:"), delete_after=15)
                        elif message.content.lower() == "nu":
                            await ctx.send(embed = Embed(color=0xff006f, description = "**Ai anulat casatoria! |** :leftwards_arrow_with_hook:"))
                        else:
                            await ctx.send(embed = Embed(color=0xff006f, description = f"**Te rog raspunde cu `DA` sau `NU` la intrebare! Incearca comanda din nou... |** :dizzy_face:"), delete_after=15)
                else: # Daca membrul este in baza (Married/unmarried)
                    if await collection.count_documents({"_id":member_id, "married":{"$exists":True}}) != 0: # Membrul este married
                        result = collection.find({"_id":member_id}, {"married":True})
                        async for i in result:
                            i_aux = i["married"]
                            if i_aux == user_id:
                                await ctx.send(embed = Embed(color=0xff006f, description = f"**Tu si** {member.mention} **sunteti deja casatoriti! |** :no_entry_sign:"), delete_after=20)
                            else:
                                await ctx.send(embed = Embed(color=0xff006f, description = f"**Membrul** {member.mention} **este deja casatorit! |** :no_entry_sign:"), delete_after=20)
                    else: # Membrul nu este married
                        await ctx.send(embed = Embed(color=0xff006f, description = f"{ctx.author.mention} **, vrei sa te casatoresti cu** {member.mention} **? (DA/NU)**"), delete_after=30)

                        try:
                            message = await self.client.wait_for("message", check = lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30.0)

                        except asyncio.TimeoutError:
                            await ctx.send(embed = Embed(color=0xff006f, description = "**Timeout |** :alarm_clock:"), delete_after=20)

                        else:
                            if message.content.lower() == "da":
                                await ctx.send(embed = Embed(color=0xff006f, description = f"{member.mention} **, vrei sa te casatoresti cu** {ctx.author.mention} **? (DA/NU)**"), delete_after=30)

                                try:
                                    message2 = await self.client.wait_for("message", check = lambda m: m.author == member and m.channel == ctx.channel, timeout=30.0)
                            
                                except asyncio.TimeoutError:
                                    await ctx.send(embed = Embed(color=0xff006f, description = "**Timeout |** :alarm_clock:"), delete_after=20)

                                else:
                                    if message2.content.lower() == "da":
                                        await collection.insert_one({"_id":user_id}) # Introdu id-ul userului in baza
                                        await collection.update_one({"_id":user_id}, {"$set":{"married":member_id}}, upsert=True)
                                        await collection.update_one({"_id":member_id}, {"$set":{"married":user_id}}, upsert=True)
                                        await collection.update_one({"_id":user_id}, {"$set":{"marrytime":date_today}})
                                        await collection.update_one({"_id":member_id}, {"$set":{"marrytime":date_today}})
                                        await ctx.send(embed = Embed(color=0xff006f, description = f"{ctx.author.mention} **si** {member.mention} **s-au casatorit! |** :white_check_mark:"))
                                    elif message2.content.lower() == "nu":
                                        await ctx.send(embed = Embed(color=0xff006f, description = "**Ai refuzat cererea in casatorie! |** :scream:"))
                                    else:
                                        await ctx.send(embed = Embed(color=0xff006f, description = f"**Te rog raspunde cu `DA` sau `NU` la intrebare! Incearca comanda din nou... |** :dizzy_face:"), delete_after=15)
                            elif message.content.lower() == "nu":
                                await ctx.send(embed = Embed(color=0xff006f, description = "**Ai anulat casatoria! |** :leftwards_arrow_with_hook:"))
                            else:
                                await ctx.send(embed = Embed(color=0xff006f, description = f"**Te rog raspunde cu `DA` sau `NU` la intrebare! Incearca comanda din nou... |** :dizzy_face:"), delete_after=15)
            elif await collection.count_documents({"_id":user_id, "married":{"$exists":True}}) == 0: # Userul este in baza si nu este married
                if await collection.count_documents({"_id":member_id}) == 0: # Membrul nu este in baza
                    await ctx.send(embed = Embed(color=0xff006f, description = f"{ctx.author.mention} **, vrei sa te casatoresti cu** {member.mention} **? (DA/NU)**"), delete_after=30)

                    try:
                        message = await self.client.wait_for("message", check = lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30.0)

                    except asyncio.TimeoutError:
                        await ctx.send(embed = Embed(color=0xff006f, description = "**Timeout |** :alarm_clock:"), delete_after=20)

                    else:
                        if message.content.lower() == "da":
                            await ctx.send(embed = Embed(color=0xff006f, description = f"{member.mention} **, vrei sa te casatoresti cu** {ctx.author.mention} **? (DA/NU)**"), delete_after=30)

                            try:
                                message2 = await self.client.wait_for("message", check = lambda m: m.author == member and m.channel == ctx.channel, timeout=30.0)
                            
                            except asyncio.TimeoutError:
                                await ctx.send(embed = Embed(color=0xff006f, description = "**Timeout |** :alarm_clock:"), delete_after=20)

                            else:
                                if message2.content.lower() == "da":
                                    await collection.update_one({"_id":user_id}, {"$set":{"married":member_id}}, upsert=True)
                                    await collection.insert_one({"_id":member_id}) # Introdu id-ul membrului in baza
                                    await collection.update_one({"_id":member_id}, {"$set":{"married":user_id}}, upsert=True)
                                    await collection.update_one({"_id":user_id}, {"$set":{"marrytime":date_today}})
                                    await collection.update_one({"_id":member_id}, {"$set":{"marrytime":date_today}})
                                    await ctx.send(embed = Embed(color=0xff006f, description = f"{ctx.author.mention} **si** {member.mention} **s-au casatorit! |** :white_check_mark:"))
                                elif message2.content.lower() == "nu":
                                    await ctx.send(embed = Embed(color=0xff006f, description = "**Ai refuzat cererea in casatorie! |** :scream:"))
                                else:
                                    await ctx.send(embed = Embed(color=0xff006f, description = f"**Te rog raspunde cu `DA` sau `NU` la intrebare! Incearca comanda din nou... |** :dizzy_face:"), delete_after=15)
                        elif message.content.lower() == "nu":
                            await ctx.send(embed = Embed(color=0xff006f, description = "**Ai anulat casatoria! |** :leftwards_arrow_with_hook:"))
                        else:
                            await ctx.send(embed = Embed(color=0xff006f, description = f"**Te rog raspunde cu `DA` sau `NU` la intrebare! Incearca comanda din nou... |** :dizzy_face:"), delete_after=15)
                else: # Membrul este in baza
                    if await collection.count_documents({"_id":member_id, "married":{"$exists":True}}) != 0: # Membrul este married
                        result = collection.find({"_id":member_id}, {"married":True})
                        async for i in result:
                            i_aux = i["married"]
                            if i_aux == user_id:
                                await ctx.send(embed = Embed(color=0xff006f, description = f"**Tu si** {member.mention} **sunteti deja casatoriti! |** :no_entry_sign:"), delete_after=20)
                            else:
                                await ctx.send(embed = Embed(color=0xff006f, description = f"**Membrul** {member.mention} **este deja casatorit! |** :no_entry_sign:"), delete_after=20)
                    else: # Membrul nu este married
                        await ctx.send(embed = Embed(color=0xff006f, description = f"{ctx.author.mention} **, vrei sa te casatoresti cu** {member.mention} **? (DA/NU)**"), delete_after=30)

                        try:
                            message = await self.client.wait_for("message", check = lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30.0)

                        except asyncio.TimeoutError:
                            await ctx.send(embed = Embed(color=0xff006f, description = "**Timeout |** :alarm_clock:"), delete_after=20)

                        else:
                            if message.content.lower() == "da":
                                await ctx.send(embed = Embed(color=0xff006f, description = f"{member.mention} **, vrei sa te casatoresti cu** {ctx.author.mention} **? (DA/NU)**"), delete_after=30)

                                try:
                                    message2 = await self.client.wait_for("message", check = lambda m: m.author == member and m.channel == ctx.channel, timeout=30.0)
                            
                                except asyncio.TimeoutError:
                                    await ctx.send(embed = Embed(color=0xff006f, description = "**Timeout |** :alarm_clock:"), delete_after=20)

                                else:
                                    if message2.content.lower() == "da":
                                        await collection.update_one({"_id":user_id}, {"$set":{"married":member_id}}, upsert=True)
                                        await collection.update_one({"_id":member_id}, {"$set":{"married":user_id}}, upsert=True)
                                        await collection.update_one({"_id":user_id}, {"$set":{"marrytime":date_today}})
                                        await collection.update_one({"_id":member_id}, {"$set":{"marrytime":date_today}})
                                        await ctx.send(embed = Embed(color=0xff006f, description = f"{ctx.author.mention} **si** {member.mention} **s-au casatorit! |** :white_check_mark:"))
                                    elif message2.content.lower() == "nu":
                                        await ctx.send(embed = Embed(color=0xff006f, description = "**Ai refuzat cererea in casatorie! |** :scream:"))
                                    else:
                                        await ctx.send(embed = Embed(color=0xff006f, description = f"**Te rog raspunde cu `DA` sau `NU` la intrebare! Incearca comanda din nou... |** :dizzy_face:"), delete_after=15)
                            elif message.content.lower() == "nu":
                                await ctx.send(embed = Embed(color=0xff006f, description = "**Ai anulat casatoria! |** :leftwards_arrow_with_hook:"))
                            else:
                                await ctx.send(embed = Embed(color=0xff006f, description = f"**Te rog raspunde cu `DA` sau `NU` la intrebare! Incearca comanda din nou... |** :dizzy_face:"), delete_after=15)
            elif await collection.count_documents({"_id":user_id, "married":{"$exists":True}}) != 0: # Userul este in baza si este married
                if await collection.count_documents({"_id":member_id}) == 0: # Membrul nu este in baza == unmarried
                    await ctx.send(embed = Embed(color=0xff006f, description = f"**Esti deja casatorit! |** :no_entry_sign:"), delete_after=20)
                else: # Membrul este in baza
                    if await collection.count_documents({"_id":member_id, "married":{"$exists":True}}) != 0: # Membrul este married
                        result = collection.find({"_id":member_id}, {"married":True})
                        gui = self.client.get_guild(id = 569077625826443274)
                        async for i in result:
                            i_aux = i["married"]
                            if i_aux == user_id:
                                await ctx.send(embed = Embed(color=0xff006f, description = f"**Tu si** {member.mention} **sunteti deja casatoriti! |** :no_entry_sign:"), delete_after=20)
                            else:
                                married_to = gui.get_member(user_id = i_aux)
                                await ctx.send(embed = Embed(color=0xff006f, description = f"{member.mention} **este deja casatorit iar tu la fel |** :no_entry_sign:"), delete_after=20)
                    else: # Membrul nu este married
                        await ctx.send(embed = Embed(color=0xff006f, description = f"**Esti deja casatorit! |** :no_entry_sign:"), delete_after=20)

    @marry.error
    async def marry_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(embed = Embed(color=0xff006f, description = f"**Incearca din nou in 30 secunde! |** :clock1:"), delete_after=10)

    @whomarried.error
    async def whomarried_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(embed = Embed(color=0xff006f, description = f"**Incearca din nou in 30 secunde! |** :clock1:"), delete_after=10)

    @divorce.error
    async def divorce_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(embed = Embed(color=0xff006f, description = f"**Incearca din nou in 30 secunde! |** :clock1:"), delete_after=10)

def setup(client):
    client.add_cog(Marry(client))