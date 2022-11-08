import discord
import motor.motor_asyncio
from discord.ext import commands
from discord import Embed

mongoURL = ""
cluster = motor.motor_asyncio.AsyncIOMotorClient(mongoURL)
db = cluster["phoenixDB"]
collection = db["phoenixCollection"]

class Afk(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        user_id = message.author.id
        user_obj = message.author

        # Daca membrul AFK scrie : 
        if await collection.count_documents({"_id":user_id, "afk":{"$exists":True}}) != 0:
            # Daca exista fieldul "afk" in documentul autorului

            # Scoate fieldul "afk"
            collection.update_one({"_id":user_id}, {"$unset":{"afk":1}})

            # Verificam daca a mai ramas doar id-ul in documentul autorului
            result = collection.find({"_id":user_id}, {"_id":1})
            result2 = collection.find({"_id":user_id})
            async for i in result:
                async for i2 in result2:
                    if i == i2:
                        # Daca da, sterge documentul
                        await collection.delete_one({"_id":user_id})
            # Afiseaza ca autorul nu mai este AFK
            await message.channel.send(embed = Embed(color = 0xe03a3e, description = f"**Membrul** {user_obj.mention} **nu mai este afk. |** <:bfa_peek:884856540190900335>"), delete_after = 15)
            

        # Daca membrul AFK este mentionat :
        if message.author.bot == 0:
            # Ne asiguram daca nu a fost mentionat de catre un BOT

            # Cautam cei care sunt AFK
            result = collection.find({"afk":{"$exists":True}}, {"afk":True})
            async for i in result:
                i_aux = i["_id"]
                i_aux_reason = i["afk"]
                gui = self.client.get_guild(id = 569077625826443274)
                user_obj_aux = gui.get_member(user_id = i_aux)

                if user_obj_aux.nick != None:
                    # Daca membrul mentionat are nickname
                    if (user_obj_aux.nick.lower() in message.content.lower()):
                        # Daca nicknameul membrului exista in mesaj
                        await message.channel.send(embed = Embed(color = 0xe03a3e, description = f"**Membrul** {user_obj_aux.mention} **este afk! Motiv:** `{i_aux_reason}` **. |** <a:blk_thunder:877666207942201396>"), delete_after = 15)    
                
                if (user_obj_aux.name.lower() in message.content.lower()):
                    # Daca numele membrului exista in mesaj
                    await message.channel.send(embed = Embed(color = 0xe03a3e, description = f"**Membrul** {user_obj_aux.mention} **este afk! Motiv:** `{i_aux_reason}` **. |** <a:blk_thunder:877666207942201396>"), delete_after = 15)
                
                if user_obj_aux in message.mentions:
                    # Daca membrul a fost mentionat in mesaj
                    await message.channel.send(embed = Embed(color=0xe03a3e, description = f"**Membrul** {user_obj_aux.mention} **este afk! Motiv:** `{i_aux_reason}` **. |** <a:blk_thunder:877666207942201396>"), delete_after = 15)

    @commands.command()
    @commands.cooldown(3, 30, commands.BucketType.user)
    async def afk(self, ctx, *, reason : str = None):
        user_id = ctx.author.id
        user_obj = ctx.author

        # Daca documentul userului nu exista
        if await collection.count_documents({"_id":user_id}) == 0:
            # Cream documentul
            await collection.insert_one({"_id":user_id})

        # In momentul acesta, documentul userului exista. Exista fieldul "afk" in document?
        if await collection.count_documents({"_id":user_id, "afk":{"$exists":True}}) == 0:
            # Daca nu exista fieldul "afk"
            # Cream fieldul "afk" in documentul userului
            collection.update_one({"_id":user_id}, {"$set":{"afk":f"{reason}"}})
            await ctx.send(embed = Embed(color = 0xe03a3e, description = f"**Membrul** {user_obj.mention} **este afk. Motiv :** `{reason}` **. |** <a:blk_thunder:877666207942201396>"), delete_after = 60)

def setup(client):
    client.add_cog(Afk(client))