import discord
from discord.ext import commands, tasks
from discord import Embed, Emoji

class Kick(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        embedDM = Embed(color=0xff006f, title=f":white_circle: **Ai luat kick de pe server. |** :anger:", description="**Motiv: **"+str(reason))
        await member.send(embed=embedDM)
        await member.send(content="**Invite link:** https://discord.gg/9KMCrpv")
        await member.kick(reason=reason)
        embed = Embed(color=0xff006f , description=f":white_circle: **{ctx.message.author.display_name}, ai dat kick membrului {member}. |** :white_check_mark:")
        await ctx.send(embed=embed)
        channel = self.client.get_channel(583619328625344512)
        embed = Embed(color=0xff006f, title=f":white_circle: **Membrul {member} a fost dat afara de catre {ctx.message.author.display_name}. |** :white_check_mark:", description="**Motiv: **"+str(reason))
        await channel.send(embed=embed)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, CheckFailure):
            embed = Embed(color=0xff006f, description=f":white_circle: **{ctx.message.author.display_name}, nu ai permisiunea sa dai afara acest membru. |** :no_entry:")
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Kick(client))
