import discord

from discord.ext import commands
from discord import Embed

sniped = ""
author = ""

class Snipe(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        global sniped
        global author
        
        sniped = message.content
        author = message.author.id

    @commands.command()
    async def snipe(self, ctx):
        global sniped
        global author
        author_obj = await self.client.fetch_user(author)

        if len(sniped) == 0:
            await ctx.send(embed = Embed(description = "**Nothing to snipe.**", color = 0xffb20c))
        else:
            await ctx.send(embed = Embed(description = f"**Message Sniped :** {sniped} \n**Author :** {author_obj.mention}", color = 0xffb20c))

def setup(client):
    client.add_cog(Snipe(client))