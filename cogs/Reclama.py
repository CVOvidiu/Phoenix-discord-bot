#TODO: Integrare Warnuri 

import discord
from discord.ext import commands
from discord import Embed

class Reclama(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        author = message.author

        if author.bot == 0 and author.id != 732756872473477142:
            # Daca reclama nu a fost facuta de un BOT sau de catre iLectus
            e1 = Embed(color=0xffb20c , description=f":white_circle: **{author.mention} a fost banat. Motiv: Reclama |** :white_check_mark:")
            e2 = Embed(color=0xffb20c, title=f":white_circle: **Membrul {author} a fost banat. |** :white_check_mark:", description="**Motiv: Reclama**")
            eDM = Embed(color=0xffb20c, title=f":white_circle: **Ai fost banat pe server. |** :no_entry:", description="**Motiv: Reclama**")
            punishment_c = self.client.get_channel(583619328625344512)
            general_c = self.client.get_channel(569077625826443276)

            if message.channel.id == '842033718424109116':
                return
            elif "https://discord.gg/" in message.content or "discord.gg/" in message.content:
                await author.send(embed=eDM)
                await author.ban()
                await general_c.send(embed=e1)
                await punishment_c.send(embed=e2)

def setup(client):
    client.add_cog(Reclama(client))