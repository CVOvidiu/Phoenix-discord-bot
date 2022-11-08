import discord
import random
import motor.motor_asyncio
from discord.ext import commands, tasks

from discord import Embed, Emoji
from discord.utils import get

mongoURL = ""
cluster = motor.motor_asyncio.AsyncIOMotorClient(mongoURL)
db = cluster["phoenixDB"]
collection_inter = db["phoenixInteractions"]

class Kiss(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def kiss(self, ctx, *, member : discord.Member):
        responses = ['']

        global collection_inter
        global db
        global cluster
        global mongoURL
        kiss_Interaction = str(ctx.author.id)+'&'+str(member.id) # cautare si invers
        kiss_Interaction_r = str(member.id)+'&'+str(ctx.author.id)
        db_kiss_Interaction = {"_id":kiss_Interaction}
        db_kiss_Interaction_2 = {"_id":kiss_Interaction_r}
        tag = discord.utils.get(ctx.guild.roles, id = 835853720175902730)

        if not tag in ctx.message.author.roles:
            
            if await collection_inter.count_documents(db_kiss_Interaction) == 0 and await collection_inter.count_documents(db_kiss_Interaction_2) == 0: # interactiune noua
                await collection_inter.insert_one({"_id":kiss_Interaction, "kisses":1})
                await collection_inter.insert_one({"_id":kiss_Interaction_r, "kisses":1})

                embed = Embed(color=0xff006f, description=f'{ctx.author.mention} **a sarutat pe** {member.mention} **pentru prima oara!** :scream:')
                embed.set_image(url=f'{random.choice(responses)}')
                await ctx.send(embed=embed)
            else:
                inter_1 = collection_inter.find(db_kiss_Interaction)
                inter_2 = collection_inter.find(db_kiss_Interaction_2)
                
                async for i in inter_1:
                    inter_inter_1 = i["kisses"]
                    inter_inter_1_upt = inter_inter_1 + 1

                async for i in inter_2:
                    inter_inter_2 = i["kisses"]
                    inter_inter_2_upt = inter_inter_2 + 1

                await collection_inter.update_one({"_id":kiss_Interaction}, {"$set":{"kisses":inter_inter_2_upt}}, upsert=True)
                await collection_inter.update_one({"_id":kiss_Interaction_r}, {"$set":{"kisses":inter_inter_1_upt}}, upsert=True)
                embed = Embed(color=0xff006f, description=f'{ctx.author.mention} **a sarutat pe** {member.mention} **!** :heart:')
                embed.set_image(url=f'{random.choice(responses)}')
                await ctx.send(embed=embed)
            # if 582267057194795018 or 569077625826443276 == ctx.message.channel.id:
            #     await await ctx.send(embed=embed)
            # else:
            #     await ctx.message.delete()
            #     await ctx.send(f"**{ctx.message.author.display_name}, scrie pe textchannel-ul potrivit!**", delete_after=5)
        else: # are tag
            if await collection_inter.count_documents(db_kiss_Interaction) == 0 and await collection_inter.count_documents(db_kiss_Interaction_2) == 0: # interactiune noua
                await collection_inter.insert_one({"_id":kiss_Interaction, "kisses":1})
                await collection_inter.insert_one({"_id":kiss_Interaction_r, "kisses":1})
                embed = Embed(color=0xff006f, description=f'{ctx.author.mention} **a sarutat pe** {member.mention} **pentru prima oara!** :scream:')
                embed.set_image(url=f'{random.choice(responses)}')
                await ctx.send(embed=embed)
            
            else: # nu e primul sarut
                inter_1 = collection_inter.find(db_kiss_Interaction)
                inter_2 = collection_inter.find(db_kiss_Interaction_2)

                async for i in inter_1:
                    inter_inter_1 = i["kisses"]
                    inter_inter_1_upt = inter_inter_1 + 1

                async for i in inter_2:
                    inter_inter_2 = i["kisses"]
                    inter_inter_2_upt = inter_inter_2 + 1

                await collection_inter.update_one({"_id":kiss_Interaction}, {"$set":{"kisses":inter_inter_2_upt}}, upsert=True)
                await collection_inter.update_one({"_id":kiss_Interaction_r}, {"$set":{"kisses":inter_inter_1_upt}}, upsert=True)
                embed = Embed(color=0xff006f, description=f'{ctx.author.mention} **si** {member.mention} **s-au sarutat de {inter_inter_1_upt} ori!** :heart:')
                embed.set_image(url=f'{random.choice(responses)}')
                await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Kiss(client))
