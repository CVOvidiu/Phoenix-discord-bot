import discord #
from discord.ext import commands
from discord import Embed, Emoji
from discord.ext.commands.core import command

class Say(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['s'])
    @commands.has_permissions(ban_members=True)
    async def say(self, ctx, *, message : str):
        await ctx.message.delete()
        await ctx.send(f'{str(message)}')

    @commands.command(aliases=['e'])
    @commands.has_permissions(ban_members=True)
    async def embed(self, ctx, colore, *, message : str):
        colore = int(colore, 16)
        embed = Embed(color=colore, description=str(message))
        await ctx.message.delete()
        await ctx.send(embed=embed)

    @commands.command(aliases=['et'])
    @commands.has_permissions(ban_members=True)
    async def embedtitle(self, ctx, colore, title : str, *, message : str):
        colore = int(colore, 16)
        embed = Embed(color=colore, title=str(title), description=str(message))
        await ctx.message.delete()
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Say(client))
