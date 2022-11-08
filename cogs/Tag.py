import discord
import datetime
import asyncio
import motor.motor_asyncio
from discord.ext import commands, tasks
from discord.utils import get
from discord import Embed, Emoji
from discord.ext.commands import BucketType, cooldown, CommandOnCooldown

taggers = 0

mongoURL = ""
cluster = motor.motor_asyncio.AsyncIOMotorClient(mongoURL)
db = cluster["phoenixDB"]
collection = db["TagTime"]

class Tag(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.last_timeStamp = datetime.datetime.utcfromtimestamp(0)

    @tasks.loop(minutes = 10)
    async def update_tag_channel(self):
        global taggers

        req_channel = self.client.get_channel(id = 843543274857300038)
        await req_channel.edit(name = f"•̥🉐Family • {taggers}")


    @tasks.loop(minutes = 1)
    async def tagtimetask(self):
        gui = self.client.get_guild(id = 569077625826443274)
        for member in gui.members:
            if "ﾉʙꜰᴀ" in member.name:
                result = collection.find({"_id":member.id}, {"time":True})
                async for i in result:
                    tag_time = int(i["time"])
                    tag_time_u = int(tag_time + 1)
                    await collection.update_one({"_id":member.id}, {"$set":{"time":tag_time_u}}, upsert=True)

    @commands.command()
    async def tagtime(self, ctx, member : discord.Member = None):
        if member == None:
            member = ctx.message.author

        if "ﾉʙꜰᴀ" not in member.name:
            if member.name == ctx.message.author.name:
                await ctx.send(embed = Embed(description = "Nu ai tagul pus!"))
            else:
                await ctx.send(embed = Embed(description = f"`{member.name}` nu are tagul pus."))
        else:
            result = collection.find({"_id":member.id}, {"time":True})
            async for i in result:
                tag_time = int(i["time"])
                tag_months = int(tag_time / 43200)
                tag_days = int((tag_time - tag_months * 43200) / 1440)
                tag_hours = int((tag_time - (tag_months * 43200) - (tag_days * 1440)) / 60)
                tag_minutes = int(tag_time - (tag_months * 43200) - (tag_days * 1440) - (tag_hours * 60))
                await ctx.send(embed = Embed(description = f"`{member.name}` a avut tagul pentru : `{tag_months}` luni, `{tag_days}` zile, `{tag_hours}` ore si `{tag_minutes}` minute."))

    @commands.Cog.listener()
    async def on_message(self, message):
        emoji = self.client.get_emoji(772122860592431125)
        if "tag" in message.content.lower() and message.author.bot == 0: 
            if "ph?tagtime" in message.content.lower():
                return
            time_difference = (datetime.datetime.utcnow() - self.last_timeStamp).total_seconds()
            if time_difference < 120:
                return
            else:
                embed = Embed(description=f'**Daca pui tagul** `ﾉʙꜰᴀ` **in nume primesti:** \n <:bfa_arrow:884870037586980944> _Gradul_ `Family` \n <:bfa_arrow:884870037586980944> _Acces la grade de culoare_ \n <:bfa_arrow:884870037586980944> _Sansa sa primesti mai mult din comanda de daily_', color=0xe03a3e)
                await message.channel.send(embed=embed, delete_after=60*5)
                self.last_timeStamp = datetime.datetime.utcnow()

    @commands.Cog.listener()
    async def on_ready(self):
        global taggers
        gui = self.client.get_guild(id = 569077625826443274)
        logs = self.client.get_channel(id = 877659413643657276)

        for member in gui.members:
            if "ﾉʙꜰᴀ" in member.name:
                taggers += 1
                if await collection.count_documents({"_id":member.id}) == 0:
                    await collection.insert_one({"_id":member.id})
                    await collection.update_one({"_id":member.id}, {"$set":{"time":0}}, upsert=True)
        await logs.send(embed = Embed(description = f"<a:loading_color:877665020949954611> | Taggers loaded : `{taggers}` loaded."))
        self.tagtimetask.start()
        self.update_tag_channel.start()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        global taggers
        ide = member.id
        gui = self.client.get_guild(id = 569077625826443274)
        role = discord.utils.get(gui.roles, id = 835853720175902730)
        logs = self.client.get_channel(id = 877659413643657276)

        if "ﾉʙꜰᴀ" in member.name:
            taggers += 1
            await member.add_roles(role)
            await logs.send(embed = Embed(description = f"<a:wings_1:877665716952789003> | `{member.name}` joined with tag."))
            
            await collection.insert_one({"_id":ide})
            await collection.update_one({"_id":ide}, {"$set":{"time":0}}, upsert=True)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        global taggers
        ide = member.id
        gui = self.client.get_guild(id = 569077625826443274)
        logs = self.client.get_channel(id = 877659413643657276)

        if "ﾉʙꜰᴀ" in member.name:
            taggers -= 1
            await logs.send(embed = Embed(description = f"<a:blk_thunder:877666207942201396> | `{member.name}` left with tag."))

            await collection.delete_one({"_id":ide})

    @commands.Cog.listener()
    async def on_user_update(self, before, after): # after - User
        global taggers
        ide = after.id
        gui = self.client.get_guild(id = 569077625826443274)
        role = discord.utils.get(gui.roles, id = 835853720175902730)
        member = gui.get_member(user_id = ide)
        logs = self.client.get_channel(id = 877659413643657276)

        if "ﾉʙꜰᴀ" not in before.name and "ﾉʙꜰᴀ" in after.name:
            taggers += 1
            await member.add_roles(role)
            await logs.send(embed = Embed(description = f"<a:blk_heart:877666480718762026> | `{before.display_name}` has put on tag."))

            await collection.insert_one({"_id":ide})
            await collection.update_one({"_id":ide}, {"$set":{"time":0}}, upsert=True)

        if "ﾉʙꜰᴀ" in before.name and "ﾉʙꜰᴀ" not in after.name:
            taggers -= 1
            await member.remove_roles(role)
            await logs.send(embed = Embed(description = f"<a:blk_moon:877666889684365372> | `{before.display_name}` took out tag."))

            await collection.delete_one({"_id":ide})

def setup(client):
    client.add_cog(Tag(client))
