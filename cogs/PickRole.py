import discord
import asyncio
from discord.ext import commands
from discord.ext.commands.core import command

class PickRole(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def hobby(self, ctx, hobby_var : str):
        hobbies = {}
        hobbies["gaming"] = discord.utils.get(ctx.guild.roles, id = 836967291778367538)
        hobbies["cooking"] = discord.utils.get(ctx.guild.roles, id = 836968512869892147)
        hobbies["music"] = discord.utils.get(ctx.guild.roles, id = 836990861312131083)
        hobbies["makeup"] = discord.utils.get(ctx.guild.roles, id = 836991426536407040)
        hobbies["photography"] = discord.utils.get(ctx.guild.roles, id = 836992122942521384)
        hobbies["sports"] = discord.utils.get(ctx.guild.roles, id = 837675996240543766)
        hobbies["programming"] = discord.utils.get(ctx.guild.roles, id = 837676554719985707)
        hobbies["graphics"] = discord.utils.get(ctx.guild.roles, id = 837677285758468168)
        hobbies["socializing"] = discord.utils.get(ctx.guild.roles, id = 837677703272333352)
        hobbies["anime"] = discord.utils.get(ctx.guild.roles, id = 837679158590832640)
        hobbies["seriale/filme"] = discord.utils.get(ctx.guild.roles, id = 838043758518992916)
        hobbies["reading"] = discord.utils.get(ctx.guild.roles, id = 838047082359029770)
        hobbies["arts"] = discord.utils.get(ctx.guild.roles, id = 838047590724534292)
        hobbies["dancing"] = discord.utils.get(ctx.guild.roles, id = 838048212597473350)
        hobbies["learning"] = discord.utils.get(ctx.guild.roles, id = 884811041354153995)

        if hobby_var.lower() not in hobbies.keys():
            await ctx.send(f"`{hobby_var}` **not in hobby list.**")
        elif hobby_var.lower() in hobbies.keys():
            role = hobbies[hobby_var.lower()]
            if role in ctx.message.author.roles:
                await ctx.message.author.remove_roles(role)
                await ctx.send(f"`{hobby_var.lower()}` **: Hobby-ul a fost scos.**")
            else:
                await ctx.message.author.add_roles(role)
                await ctx.send(f"`{hobby_var.lower()}` **: Hobby-ul a fost adaugat.**")

    @commands.command()
    async def toggle(self, ctx, field : str):
        toggles = {}
        toggles["archive"] = discord.utils.get(ctx.guild.roles, id = 884832671459590164)
        toggles["playlist"] = discord.utils.get(ctx.guild.roles, id = 884832580808089600)
        toggles["welcomeleave"] = discord.utils.get(ctx.guild.roles, id = 884831779008184330)
        toggles["colab"] = discord.utils.get(ctx.guild.roles, id = 878964297986900018)
        toggles["leveling"] = discord.utils.get(ctx.guild.roles, id = 884830943355994162)
        toggles["boost"] = discord.utils.get(ctx.guild.roles, id = 884831287507030027)
        toggles["punishroom"] = discord.utils.get(ctx.guild.roles, id = 884831502301540473)
        toggles["suggestions"] = discord.utils.get(ctx.guild.roles, id = 884832149964984422)

        if field.lower() not in toggles.keys():
            await ctx.send(f"`{field.lower()}` **not in toggle list.**")
        elif field.lower() in toggles.keys():
            role = toggles[field.lower()]
            if role in ctx.message.author.roles:
                await ctx.message.author.remove_roles(role)
                await ctx.send(f"`{field.lower()}-on` **: Primesti notificari de pe acest canal.**")
            else:
                await ctx.message.author.add_roles(role)
                await ctx.send(f"`{field.lower()}-off` **: Nu mai primesti notificari de pe acest canal.**")

    @commands.command()
    async def games(self, ctx, game : str):
        games = {}
        games["mudae"] = discord.utils.get(ctx.guild.roles, id = 884817129906520085)

        if game.lower() not in games.keys():
            await ctx.send(f"`{game.lower()}` **not in game list.**")
        elif game.lower() in games.keys():
            role = games[game.lower()]
            if role in ctx.message.author.roles:
                await ctx.message.author.remove_roles(role)
                await ctx.send(f"`{game.lower()}-off` **: Nu mai poti sa joci acest joc.**")
            else:
                await ctx.message.author.add_roles(role)
                await ctx.send(f"`{game.lower()}-access` **: Poti sa joci acest joc.**")

def setup(client):
    client.add_cog(PickRole(client))