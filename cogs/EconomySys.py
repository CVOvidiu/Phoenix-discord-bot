import discord
import asyncio

from discord import user
from discord.ext.commands.core import command
import motor.motor_asyncio
import random
from discord.ext import commands, tasks
from discord import Embed, Emoji
from discord.ext.commands import BucketType

mongoURL = ""
cluster = motor.motor_asyncio.AsyncIOMotorClient(mongoURL)
db = cluster["phoenixDB"]
collection = db["phoenixCollection"]
events = db["UserRuningEvents"]

class EconomySys(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['p', 'givemoney', 'gm'])
    @commands.cooldown(3, 30, commands.BucketType.user)
    async def pay(self, ctx, member : discord.Member, credits : int):
        global collection
        global db
        global cluster
        global mongoURL
        user_id = ctx.author.id
        member_id = member.id
        gui = self.client.get_guild(id = 569077625826443274)
        mem_mention = gui.get_member(user_id = member_id)

        if credits >= 100:
            if await collection.count_documents({"_id":user_id}) == 0: # userul nu se afla in baza
                await ctx.send(embed = Embed(color=0xe03a3e, description = "**Nu poti sa faci asta, balanta ta este :** `0` <:currency:800676742104088578> **! |**:no_entry_sign:"))
            else: # userul este in baza
                if await collection.count_documents({"_id":user_id, "balance":{"$exists":True}}) != 0: # inseamna ca fieldul balanta exista in user data
                
                    result = collection.find({"_id":user_id}, {"balance":True})
                    async for i in result:
                        bal = i["balance"]
                        if bal == 0:
                            await ctx.send(embed = Embed(color=0xe03a3e, description = "**Nu poti sa faci asta, balanta ta este :** `0` <:currency:800676742104088578> **! |**:no_entry_sign:"))
                        elif bal < 50:
                            await ctx.send(embed = Embed(color=0xe03a3e, description = "**Ai prea putine** <:currency:800676742104088578> **pentru a efectua aceasta comanda! |** :chart_with_downwards_trend:"))
                        else:
                            taxed_credits = int(credits - ((15*credits)/100))
                            updated_bal = bal - credits
                            await ctx.send(embed = Embed(color=0xe03a3e, description = f"**Esti sigur ca vrei sa faci asta? {mem_mention.mention} o sa primeasca doar** `{taxed_credits}` <:currency:800676742104088578> **(Taxa 15%)! (DA/NU) |** :warning:"))
                            try:
                                message = await self.client.wait_for("message", check = lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30.0)
                            except asyncio.TimeoutError:
                                await ctx.send(embed = Embed(color=0xe03a3e, description = "**Timeout |** :alarm_clock:"))
                            else:
                                if message.content.lower() == "da":
                                    if await collection.count_documents({"_id":member_id}) == 0: # membrul nu este in baza
                                        await collection.insert_one({"_id":member_id})
                                        await collection.update_one({"_id":member_id}, {"$set":{"balance":0}}, upsert=True)
                                    # credits e suma de dat
                                    await collection.update_one({"_id":user_id}, {"$set":{"balance":updated_bal}}, upsert=True)
                                    result2 = collection.find({"_id":member_id}, {"balance":True})
                                    async for i2 in result2:
                                        mem_actual_bal = i2["balance"]
                                        mem_updated_bal = mem_actual_bal + taxed_credits
                                        await collection.update_one({"_id":member_id}, {"$set":{"balance":mem_updated_bal}}, upsert=True)
                                    await ctx.send(embed = Embed(color=0xe03a3e, description = f"**Tranzactie reusita! {ctx.author.mention} i-a dat membrului {mem_mention.mention}** `{taxed_credits}` <:currency:800676742104088578> **! (Taxa 15%) |** :white_check_mark:"))
                                elif message.content.lower() == "nu":
                                    await ctx.send(embed = Embed(color=0xe03a3e, description = f"**Ai anulat tranzactia! |** :leftwards_arrow_with_hook:"))
                                else:
                                    await ctx.send(embed = Embed(color=0xe03a3e, description = f"**Te rog raspunde cu `DA` sau `NU` la intrebare! Incearca comanda din nou... |** :dizzy_face:"))
                else: # fieldul balanta nu exista in user data
                    await ctx.send(embed = Embed(color=0xe03a3e, description = "**Nu poti sa faci asta, balanta ta este :** `0` <:currency:800676742104088578> **! |**:no_entry_sign:"))
        else:
            await ctx.send(embed = Embed(color=0xe03a3e, description = "**Nu poti sa oferi o suma mai mica de** `100` <:currency:800676742104088578> **! |** :no_entry_sign:"))

    @commands.command(aliases=['bal', 'money', 'credits'])
    @commands.cooldown(3, 30, commands.BucketType.user)
    async def balance(self, ctx, member : discord.Member = None):
        global collection
        global db
        global cluster
        global mongoURL
        user_id = ctx.author.id

        if(member == None): # membrul nu este specificat
            if await collection.count_documents({"_id":user_id}) == 0: # Nu este in baza
                await ctx.send(embed = Embed(color=0xe03a3e, description = "**Balanta ta este :** `0` <:currency:800676742104088578>"))
            else: # este in baza - Nu are balanta sau are balanta
                if await collection.count_documents({"_id":user_id, "balance":{"$exists":True}}) == 0: # Nu exista balance in documente
                    await ctx.send(embed = Embed(color=0xe03a3e, description = "**Balanta ta este :** `0` <:currency:800676742104088578>"))
                else: # Exista fieldul balance in documentul userului
                    result = collection.find({"_id":user_id}, {"balance":True})
                    async for i in result:
                        bal = int(i["balance"])
                        await ctx.send(embed = Embed(color=0xe03a3e, description = f'**Balanta ta este :** `{bal}` <:currency:800676742104088578>'))
        else: # membrul este specificat - este in baza(are sau nu balanta) sau nu
            member_id = member.id
            gui = self.client.get_guild(id = 569077625826443274)
            mem_mention = gui.get_member(user_id = member_id)
            if await collection.count_documents({"_id":member_id}) == 0: # Nu este in baza
                await ctx.send(embed = Embed(color=0xe03a3e, description = f"**Balanta membrului {mem_mention.mention} este :** `0` <:currency:800676742104088578>"))
            else: # este in baza - Nu are balanta sau are balanta
                if await collection.count_documents({"_id":member_id, "balance":{"$exists":True}}) == 0: # Nu exista balance in documente
                    await ctx.send(embed = Embed(color=0xe03a3e, description = f"**Balanta membrului {mem_mention.mention} este :** `0` <:currency:800676742104088578>"))
                else: # Exista fieldul balance in documentul userului
                    result = collection.find({"_id":member_id}, {"balance":True})
                    async for i in result:
                        bal = int(i["balance"])
                        await ctx.send(embed = Embed(color=0xe03a3e, description = f'**Balanta membrului {mem_mention.mention} este :** `{bal}` <:currency:800676742104088578>'))

    @commands.command()
    @commands.is_owner()
    async def take(self, ctx, credits : int, member : discord.Member):
        global collection
        global db
        global cluster
        global mongoURL
        member_id = member.id

        if await collection.count_documents({"_id":member_id}) == 0: # membrul nu este in baza
            await ctx.send(embed = Embed(color=0xe03a3e, description = "**Nu poti sa faci asta, membrul nu este in baza de date! |** :no_entry_sign:"))
        else: # membrul este in baza
            if await collection.count_documents({"_id":member_id, "balance":{"$exists":True}}) == 0: # Nu exista balance in documente
                await ctx.send(embed = Embed(color=0xe03a3e, description = "**Nu poti sa faci asta, fieldul `balance` nu exista in documentul din baza de date a membrului! |** :no_entry_sign:"))
            else: # Exista fieldul
                result = collection.find({"_id":member_id}, {"balance":True})
                async for i in result:
                    bal_actual = i["balance"]
                    bal_updated = round(bal_actual - credits, 2)
                    if bal_updated <= 0:
                        await collection.update_one({"_id":member_id}, {"$unset":{"balance":1}})
                        just_id = collection.find({"_id":member_id}, {"_id":1})
                        raw_data = collection.find({"_id":member_id})
                        async for i2 in just_id:
                            async for i3 in raw_data:
                                if i2 == i3: # are doar id-ul
                                    await collection.delete_one({"_id":member_id})
                    else:
                        await collection.update_one({"_id":member_id}, {"$set":{"balance":bal_updated}}, upsert=True)
                    await ctx.send(embed = Embed(color=0xe03a3e, description = f"**{ctx.author.mention} i-a luat membrului {member.mention} `{credits}` <:currency:800676742104088578>! |** :star:"))

    @commands.command()
    @commands.is_owner()
    async def give(self, ctx, member : discord.Member, credits : int):
        global collection
        global db
        global cluster
        global mongoURL
        member_id = member.id

        if await collection.count_documents({"_id":member_id}) == 0: # membrul nu este in baza
            await collection.insert_one({"_id":member_id})
            await collection.update_one({"_id":member_id}, {"$set":{"balance":0}}, upsert=True)
            result = collection.find({"_id":member_id}, {"balance":True})
            async for i in result:
                bal_actual = i["balance"]
                bal_updated = round(bal_actual + credits, 2)
                await collection.update_one({"_id":member_id}, {"$set":{"balance":bal_updated}}, upsert=True)
                await ctx.send(embed = Embed(color=0xe03a3e, description = f"**{ctx.author.mention} i-a dat membrului {member.mention} `{credits}` <:currency:800676742104088578>! |** :star:"))
        else:
            if await collection.count_documents({"_id":member_id, "balance":{"$exists":True}}) == 0: # Nu exista balance in documente
                await collection.update_one({"_id":member_id}, {"$set":{"balance":0}}, upsert=True)
                result = collection.find({"_id":member_id}, {"balance":True})
                async for i in result:
                    bal_actual = i["balance"]
                    bal_updated = round(bal_actual + credits, 2)
                    await collection.update_one({"_id":member_id}, {"$set":{"balance":bal_updated}}, upsert=True)
                    await ctx.send(embed = Embed(color=0xe03a3e, description = f"**{ctx.author.mention} i-a dat membrului {member.mention} `{credits}` <:currency:800676742104088578>! |** :star:"))
            else:
                result = collection.find({"_id":member_id}, {"balance":True})
                async for i in result:
                    bal_actual = i["balance"]
                    bal_updated = round(bal_actual + credits, 2)
                    await collection.update_one({"_id":member_id}, {"$set":{"balance":bal_updated}}, upsert=True)
                    await ctx.send(embed = Embed(color=0xe03a3e, description = f"**{ctx.author.mention} i-a dat membrului {member.mention} `{credits}` <:currency:800676742104088578>! |** :star:"))


    # Credite pe Mesaj
    @commands.Cog.listener()
    async def on_message(self, message):
        global collection
        global db
        global cluster
        global mongoURL
        suma_msg_non = int(round(random.uniform(1, 3)))
        suma_msg = int(round(random.uniform(1, 6)))
        user_id = message.author.id

        if "ﾉʙꜰᴀ" not in message.author.name and message.author.bot == 0:
            if await collection.count_documents({"_id":user_id}) == 0: # Nu este in baza
                await collection.insert_one({"_id":user_id})
                await collection.update_one({"_id":user_id}, {"$set":{"balance":0}}, upsert = True)

            # Acum e in baza
            result = collection.find({"_id":user_id}, {"balance":True})
            async for i in result:
                bal_actual = i["balance"]
                bal_updated = round(bal_actual + suma_msg_non, 2)
                await collection.update_one({"_id":user_id}, {"$set":{"balance":bal_updated}}, upsert=True)
                print(f"Ball updated {message.author.name} : rand = {suma_msg_non} bal = {bal_updated}")

        elif "ﾉʙꜰᴀ" in message.author.name and message.author.bot == 0:
            if await collection.count_documents({"_id":user_id}) == 0: # Nu este in baza
                await collection.insert_one({"_id":user_id})
                await collection.update_one({"_id":user_id}, {"$set":{"balance":0}}, upsert = True)
            
            # Acum e in baza
            result = collection.find({"_id":user_id}, {"balance":True})
            async for i in result:
                bal_actual = i["balance"]
                bal_updated = round(bal_actual + suma_msg, 2)
                await collection.update_one({"_id":user_id}, {"$set":{"balance":bal_updated}}, upsert=True)
                print(f"Ball updated {message.author.name} : rand = {suma_msg} bal = {bal_updated}")

    @tasks.loop(minutes = 1)
    async def daily_check(self):
        result = events.find({"daily-cd":{"$exists":True}})
        async for i in result:
            user_id = i["_id"]
            user_cd = i["daily-cd"]
            upt_cd = user_cd - 1
            if upt_cd <= 0:
                await events.update_one({"_id":user_id}, {"$unset":{"daily-cd":1}})
            else:
                await events.update_one({"_id":user_id}, {"$set":{"daily-cd":upt_cd}})

        # Just the id in db is handled

    @commands.Cog.listener()
    async def on_ready(self):
        self.daily_check.start()

    @commands.command(aliases=['d'])
    @commands.cooldown(3, 30, commands.BucketType.user)
    async def daily(self, ctx):
        user_id = ctx.author.id
        tag = discord.utils.get(ctx.author.guild.roles, id = 835853720175902730)
        
        if await events.count_documents({"_id":user_id, "daily-cd":{"$exists":True}}) != 0:
            result = events.find({"_id":user_id}, {"daily-cd":True})
            async for i2 in result:
                timer = i2["daily-cd"]
                time_h = int(timer / 60)
                time_m = timer % 60
            await ctx.send(embed = Embed(color=0xe03a3e, description =f"**Poti sa mai folosesti comanda de daily in `{time_h}` ore si `{time_m}` minute. |** :clock1:"))
        else:
            # Ready
            if await collection.count_documents({"_id":user_id}) == 0:
                # User not in EcoDb
                await collection.insert_one({"_id":user_id})
                await collection.update_one({"_id":user_id}, {"$set":{"balance":0}})
            
            if tag in ctx.author.roles:
                suma_daily = int(round(random.uniform(250, 750)))
            else:
                suma_daily = int(round(random.uniform(1, 500)))
            cd_time = 60 * 24

            result = collection.find({"_id":user_id}, {"balance":True})
            async for i in result:
                bal_actual = i["balance"]
                bal_updated = round(bal_actual + suma_daily, 2)
                await collection.update_one({"_id":user_id}, {"$set":{"balance":bal_updated}})
                if suma_daily < (500 * 3) / 4:
                    await ctx.send(embed = Embed(color=0xe03a3e, description = f"**Ai primit** `{suma_daily}` <:currency:800676742104088578> **din daily!**"))
                else:
                    await ctx.send(embed = Embed(color=0xe03a3e, description = f"**Ai avut noroc <:bfa_wow:885137445232967690> ! Ai primit** `{suma_daily}` <:currency:800676742104088578> **din daily!**"))

            if await events.count_documents({"_id":user_id}) == 0:
                await events.insert_one({"_id":user_id})

            await events.update_one({"_id":user_id}, {"$set":{"daily-cd":cd_time}})

    @daily.error
    async def daily_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(embed = Embed(color=0xe03a3e, description = f"**Incearca din nou in 30 secunde! |** :clock1:"))

    @give.error
    async def give_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed = Embed(color=0xe03a3e, description = "**Ceva nu a mers bine! Incearca din nou : `ph?give <member> <credits>` |** :dizzy_face:"))
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed = Embed(color=0xe03a3e, description = "**Nu ai permisiunea la aceasta comanda! |** :no_entry_sign:"))

    @take.error
    async def take_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed = Embed(color=0xe03a3e, description = "**Ceva nu a mers bine! Incearca din nou : `ph?give <credits> <member>` |** :dizzy_face:"))
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed = Embed(color=0xe03a3e, description = "**Nu ai permisiunea la aceasta comanda! |** :no_entry_sign:"))

    @pay.error
    async def pay_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(embed = Embed(color=0xe03a3e, description = f"**Incearca din nou in 30 secunde! |** :clock1:"))
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed = Embed(color=0xe03a3e, description = "**Ceva nu a mers bine! Incearca din nou : `ph?pay <member> <credits>` |** :dizzy_face:"))

    @balance.error
    async def balance_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(embed = Embed(color=0xe03a3e, description = f"**Incearca din nou in 30 secunde! |** :clock1:"))

def setup(client):
    client.add_cog(EconomySys(client))