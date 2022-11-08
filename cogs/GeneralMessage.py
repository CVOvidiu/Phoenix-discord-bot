import discord
import random
from discord.ext import commands, tasks
from discord import Embed, Emoji

message_counter = 0

class GeneralMessage(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        gen = self.client.get_channel(569077625826443276)
        gaming = self.client.get_channel(638804098346516510)    
        if gen or gaming:
            global message_counter
            message_counter += 1

        if message_counter == 200:
            responses = [
                f"**Echipa BornFromAshes va ureaza distractie placuta. \n Sunteti cei mai tari. :heart:**",
                f"**TIP: Daca vrei sa ajuti serverul sa creasca, poti sa dai [!d bump] pe channelul de comenzi sau sa lasi un review pe DISBOARD.** :heart:",
                f"**TIP: Daca aveti orice problema/sugestie, contactati un Divine!**",
                f'**TIP: Vrei sa iti schimbi culoarea si nu ai bani? Poti sa iti pui tagul "ﾉʙꜰᴀ" si ai acces gratuit la culori!**',
                f'**TIP: Daca iti pui tagul "ﾉʙꜰᴀ", o sa faci parte din familia comunitatii BFA!**',
                f"**TIP: Nu uita, daca iti inviti prietenii pe server poti obtine beneficii!**"
            ]
            embed = Embed(color=0xff006f , description=f'{random.choice(responses)}')
            await gen.send(embed = embed, delete_after=5*60)
            message_counter = 0

def setup(client):
    client.add_cog(GeneralMessage(client))
