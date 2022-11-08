import discord
from discord.ext import commands
from discord import Embed

class Clear(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, amount = 10):
        await ctx.channel.purge(limit = amount)
        await ctx.send(f'**{ctx.message.author.display_name} a sters {amount} mesaje din chat!**', delete_after = 5)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = Embed(color = 0xffb20c, description = f":white_circle: **{ctx.message.author.display_name}, nu ai permisiunea sa stergi chatul. |** :no_entry:")
            await ctx.send(embed = embed, delete_after = 5)

def setup(client):
    client.add_cog(Clear(client))
