#TODO: Remake it

from asyncio.tasks import wait
import discord
from discord import guild
import motor.motor_asyncio
from discord.ext import commands, tasks
from discord import Embed
import asyncio
import random

mongoURL = ""
cluster = motor.motor_asyncio.AsyncIOMotorClient(mongoURL)
db = cluster["phoenixDB"]
collection = db["UserRuningEvents"]

class Mute(commands.Cog):
    def __init__(self, client):
        self.client = client

    @tasks.loop(minutes = 1)
    async def mute_check(self):
        punishroom = self.client.get_channel(583619328625344512)
        result = collection.find({"muted":{"$exists":True}})
        async for i in result:
            print(i)
            user_id = i["_id"]
            i_aux = i["muted"]
            old_timer = i_aux["time"]
            reason = i_aux["reason"]
            updated_timer = old_timer - 1
            if updated_timer <= 0:
                guild = self.client.get_guild(569077625826443274)
                member_obj = guild.get_member(user_id)
                muted = discord.utils.get(guild.roles, id = 835869598335238164)
                await member_obj.remove_roles(muted)
                await punishroom.send(embed = Embed(color = 0xe03a3e, description = f"**{member_obj.display_name} a luat unmute.** *Reason:* **Mute expired**"))
                await collection.update_one({"_id":user_id}, {"$unset":{"muted":1}})
            else:
                dict_string = {"time":updated_timer, "reason":reason}
                await collection.update_one({"_id":user_id}, {"$set":{"muted":dict_string}})
        
        # If just id in db
        result_2 = collection.aggregate([
            {"$addFields":{
                "count":{
                    "$size":{
                        "$objectToArray": "$$ROOT"
                    }
                }
            }}
        ])
        async for i2 in result_2:
            print(i2)
            user_id = i2["_id"]
            counter = i2["count"]
            if counter == 1:
                await collection.delete_one({"_id":user_id})

    @commands.Cog.listener()
    async def on_ready(self):
        self.mute_check.start()

    @commands.command(aliases=['m'])
    @commands.has_role(876759046336688138)
    async def mute(self, ctx, member : discord.Member, timer = 0, *, reason = None):
        muted = discord.utils.get(ctx.author.guild.roles, id = 835869598335238164)
        channel = self.client.get_channel(583619328625344512)
        staff = discord.utils.get(ctx.guild.roles, id = 876759046336688138)
        fondator = discord.utils.get(ctx.guild.roles, id = 579066160788799504)
        user_id = member.id
        
        # Self-mute
        if member.id == ctx.author.id:
            await ctx.send(embed = Embed(color = 0xe03a3e, description = f":white_circle: **{ctx.message.author.display_name}, iti da mute Lectus, daca tot vrei. |** :white_check_mark:"))
            return

        # Time is lower than 5 minutes
        if timer < 5:
            await ctx.send(embed = Embed(color = 0xe03a3e, description = f"**Timpul mute-ului nu poate fi mai mic de 5 minute.**"))
            return

        # Wants to ban STAFF member and is not fondator
        if fondator in ctx.message.author.roles:
            # Is fondator
            pass
        elif staff in member.roles:
            await ctx.send(embed = Embed(color = 0xe03a3e, description = f'**Nu poti da mute unui membru STAFF.**'))
            return

        dict_string = {"time":timer, "reason":f"{reason}"}
        if await collection.count_documents({"_id":user_id}) == 0:
            # If member is not in DB, add him
            await collection.insert_one({"_id":user_id})
        if await collection.count_documents({"_id":user_id, "muted":{"$exists":True}}) == 0:
            # If user is not muted
            await member.add_roles(muted)
            await ctx.send(embed = Embed(color=0xe03a3e , description=f":white_circle: **{ctx.message.author.display_name}, ai dat mute membrului {member.mention} pentru {timer} minute. |** :white_check_mark:"))
            await channel.send(embed = Embed(color=0xe03a3e, title=f":white_circle: **Membrul {member} a luat mute de {timer} minute de la {ctx.message.author.display_name}. |** :white_check_mark:", description="**Motiv: **"+str(reason)))
            await collection.update_one({"_id":user_id}, {"$set":{"muted":dict_string}})
            if member.voice.channel != None:
                # If user in voice, disconnect
                await member.move_to(channel = None)
        else:
            # User is already muted
            result = collection.find({"muted":{"$exists":True}})
            async for i in result:
                user_id = i["_id"]
                i_aux = i["muted"]
                time = i_aux["time"]
                updated_timer = time + timer
                dict_string = {"time":updated_timer, "reason":f"{reason}"}
                await collection.update_one({"_id":user_id}, {"$set":{"muted":dict_string}})
                await ctx.send(embed = Embed(color=0xe03a3e , description=f":white_circle: **{ctx.message.author.display_name}, i-ai prelungit mute-ul membrului {member.mention} pentru {timer} minute. |** :white_check_mark:"))
                await channel.send(embed = Embed(color=0xe03a3e, title=f":white_circle: **Mute-ul membrului {member} a fost prelungit cu {timer} minute de catre {ctx.message.author.display_name}. |** :white_check_mark:", description="**Motiv: **"+str(reason)))

    @commands.command(aliases=['um'])
    @commands.has_role(876759046336688138)
    async def unmute(self, ctx, member : discord.Member, *, reason = None):
        user_id = member.id
        if await collection.count_documents({"_id":user_id, "muted":{"$exists":True}}) == 0:
            await ctx.send(embed = Embed(color = 0xe03a3e, description = f"**Membrul nu are mute.**"))
        else:
            muted = discord.utils.get(ctx.author.guild.roles, id = 835869598335238164)
            channel = self.client.get_channel(583619328625344512)
            await member.remove_roles(muted)
            await ctx.send(embed = Embed(color=0xe03a3e , description=f":white_circle: **{ctx.message.author.display_name}, ai dat unmute membrului {member.mention}. |** :white_check_mark:"))
            await channel.send(embed = Embed(color=0xe03a3e, title=f":white_circle: **Membrul {member} a luat unmute de la {ctx.message.author.display_name}. |** :white_check_mark:", description="**Motiv: **"+str(reason)))
            await collection.update_one({"_id":user_id}, {"$unset":{"muted":1}})

        if member.voice.channel != None:
            await member.move_to(channel = None)

    @commands.command(aliases=['cm'])
    async def checkmute(self, ctx, member: discord.Member):
        user_id = member.id
        if await collection.count_documents({"_id":user_id, "muted":{"$exists":True}}) == 0:
            await ctx.send(embed = Embed(color = 0xe03a3e, description = f"**Membrul nu are mute.**"))
        else:
            result = collection.find({"_id":user_id}, {"muted":True})
            async for i in result:
                i_aux = i["muted"]
                time = i_aux["time"]
                res = i_aux["reason"]
            await ctx.send(embed = Embed(color = 0xe03a3e, description = f'**Membrul `{member}` are mute pentru {time} minute. Motiv: {res}**'))

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send(embed = Embed(color = 0xe03a3e, description = f'**Nu ai access la aceasta comanda!**'))

def setup(client):
    client.add_cog(Mute(client))
