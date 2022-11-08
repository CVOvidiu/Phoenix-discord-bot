import discord
from discord.ext import commands, tasks
from discord import Embed, Emoji
import asyncio
from discord.ext.commands import BucketType, cooldown, CommandOnCooldown

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['h'])
    @cooldown(3, 60, BucketType.user)
    async def help(self, ctx, page = 1):
        author = ctx.author

        if page == 1:
            embed = Embed(title = '**Informatii Generale**', description = 'Va multumim pentru ca ne sunteti alaturi. Pentru a lasa o sugestie in legatura cu BOT-ul, DM **iLectus** !', color = 0xe03a3e)
            embed.set_footer(text = 'Made by iLectus#3916', icon_url='https://cdn.discordapp.com/attachments/768118506813390859/804786242692579348/phoenix_Logo2.png')
            embed.add_field(name = '`ph?hug [membrul]` - Hug', value = 'Imbratiseaza pe cineva.', inline = False)
            embed.add_field(name = '`ph?kiss [membrul]` - Kiss', value = 'Saruta pe cineva. <Beneficii tag>', inline = False)
            embed.add_field(name = '`ph?kill [membrul]` - Kill', value = 'Ucide pe cineva.', inline = False)
            embed.add_field(name = '`ph?pay [membrul] [credite]` - Pay with credits', value = 'Plateste pe cineva.', inline = False)
            embed.add_field(name = '`ph?balance [(Optional)membrul]` - Credit balance', value = 'Daca e folosit fara membru, afiseaza balanta proprie, daca nu, afiseaza balanta membrului.', inline = False)
            embed.add_field(name = '`ph?daily` - Daily credits', value = 'Credite gratis la fiecare 24 de ore.', inline = False)
            embed.add_field(name = '`ph?marry [membrul]` - Marry someone', value = 'Casatoreste-te cu cineva, trebuie (sau nu) si cealalta persoana sa accepte. Daca este folosita fara membru, afiseaza statusul relatiei tale.', inline = False)
            embed.add_field(name = '`ph?whomarried [membrul]` - Who Married Him/Her', value = 'Vezi cu cine s-a casatorit membrul.', inline = False)
            embed.add_field(name = '`ph?divorce` - Divorce', value = 'Divorteaza din relatia curenta.', inline = False)
            embed.add_field(name = '`ph?help 2`', value = 'Next Page >>>', inline = False)
        elif page == 2:
            embed = Embed(color = 0xe03a3e, title = "Page 2 of help")
            embed.add_field(name = '`ph?afk [Motiv]` - AFK', value = 'Daca vrei sa stie lumea ca esti AFK.', inline = False)
            embed.add_field(name = '`ph?shop [(Optional)categorie]` - Shop', value = 'Shopul serverului.', inline = False)
            embed.add_field(name = '`ph?inventory` - Inventar', value = 'Inventarul tau', inline = False)
            embed.add_field(name = '`ph?toggle [field]` - Dezactivare pinguri', value = 'Daca vrei sa iti dezactivezi pingurile de pe un anumit canal.', inline = False)
            embed.add_field(name = '`ph?buy [obiect]` - Cumpara un obiect', value = 'Cumparare obiect din shopul serverului.', inline = False)
            embed.add_field(name = '`ph?swaptocolor [color(none)]` - Schimbare culoare', value = 'Daca vrei sa iti schimbi culoarea.', inline = False)
            embed.add_field(name = '`ph?birthday [zz/ll]` - Setare ziua nastere.', value = 'Ca sa iti setezi ziua de nastere. (DISCONTINUED)', inline = False)
            embed.set_footer(text = 'Made by iLectus#3916', icon_url='https://cdn.discordapp.com/attachments/768118506813390859/804786242692579348/phoenix_Logo2.png')
        else:
            embed = Embed(color = 0xe03a3e, title = "**Pagina asta nu exista**")
            embed.set_footer(text = 'Made by iLectus#3916', icon_url='https://cdn.discordapp.com/attachments/768118506813390859/804786242692579348/phoenix_Logo2.png')

        if 582267057194795018 == ctx.message.channel.id:
            await ctx.message.delete()
            await ctx.send(embed=embed, delete_after=60*5)
        else:
            await ctx.message.delete()
            await ctx.send(f"**{ctx.message.author.display_name}, scrie pe textchannel-ul potrivit!**", delete_after=5)

        
    @help.error
    async def help_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            await ctx.message.delete()
            embed = Embed(description=f'Command on cooldown, try again in {error.retry_after:,.2f} seconds.', color=0xff0004)
            await ctx.send(embed=embed, delete_after=5)


def setup(client):
    client.add_cog(Help(client))
