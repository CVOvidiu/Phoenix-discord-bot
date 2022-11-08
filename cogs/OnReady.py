import discord
from discord.ext import commands
from discord import Embed, Emoji

class OnReady(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        logs = self.client.get_channel(id = 877659413643657276)
        await self.client.change_presence(activity = discord.Game(name = "» ph?help | BornFromAshes «"))
        await logs.send(embed = Embed(description = "<a:firey:877664430186446908> | Bot has been restarted."))
        print("Logged in!\n----------\n")
        print(f"Connected to {len(self.client.guilds)} guilds...  {', '.join([e.name for e in self.client.guilds])}")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(embed = Embed(color = 0xe03a3e, description = "<:bfa_salt:885140648662036500> | Comanda nu exista."), delete_after = 60)

def setup(client):
    client.add_cog(OnReady(client))
