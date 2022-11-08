import discord
import random
from discord.ext import commands, tasks
from discord import Embed, Emoji

class Hug(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def hug(self, ctx, *, member : discord.Member):
        responses = ['']
        embed = Embed(color=0xff006f, title=f'**{ctx.message.author.display_name} a imbratisat pe** {member.display_name}**!** :hugging:')
        embed.set_image(url=f'{random.choice(responses)}')
        if 582267057194795018 or 569077625826443276 == ctx.message.channel.id:
            await ctx.send(embed=embed)
        else:
            await ctx.message.delete()
            await ctx.send(f"**{ctx.message.author.display_name}, scrie pe textchannel-ul potrivit!**", delete_after=5)

def setup(client):
    client.add_cog(Hug(client))
