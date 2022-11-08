
import discord
from discord.ext import commands, tasks
from discord import Embed, Emoji

class Parteneriat(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['part'])
    @commands.has_permissions(administrator=True)
    async def parteneriat(self, ctx, link : str, member : discord.Member, *, descriere : str = None):
        channel = self.client.get_channel(877231966888558612)
        desc = f"""
        <:bfa_pin:884881995702882365> **Fondator / Invite Manager :** {member.mention}
        """
        embed = Embed(color = 0xffb20c, title = '<:bfa_peek:884856540190900335> A wild partenership has appeared...', description = desc)
        await channel.send('https://cdn.discordapp.com/attachments/768118506813390859/846110459556003950/image3-1.png')
        await channel.send(embed = embed)
        if descriere != None:
            await channel.send(f"{descriere}")
        await channel.send(f'{link} @everyone')
        await channel.send('https://cdn.discordapp.com/attachments/768118506813390859/846110459556003950/image3-1.png')
        role = discord.utils.get(ctx.guild.roles, id = 878706651165777982)
        await member.add_roles(role)

def setup(client):
    client.add_cog(Parteneriat(client))
