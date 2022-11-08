import discord
from discord.ext import commands
from discord import Embed, Emoji
from discord.ext.commands import BucketType, cooldown, CommandOnCooldown

class Futures(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @cooldown(3, 60, BucketType.user)
    async def futures(self, ctx, page = 1):
        author = ctx.author

        if page == 1:
            embed = Embed(title = "**Futures**", description = 'Astea sunt toate chestiile care nu tin de comenzi (events)', color = 0xff006f)
            embed.set_footer(text = 'Made by iLectus#3916', icon_url='https://cdn.discordapp.com/attachments/768118506813390859/804786242692579348/phoenix_Logo2.png')
            embed.add_field(name = "Anti-Reclama", value = "Da ban tuturor membrilor care posteaza invite link pe server.", inline = False)
            embed.add_field(name = 'Bump announce', value = 'Anunta cand este valabil bump-ul de la DISBOARD.', inline = False)
            embed.add_field(name = 'Sistem de moderare', value = 'Clear/Ban/Unban/Kick/Mute/Unmute', inline = False)
            embed.add_field(name = 'EconomySystem', value = 'pay/balance/take/give/daily', inline = False)
            embed.add_field(name = 'GeneralMessage', value = 'Din un numar constant de mesaje in numar constant de mesaje apare un mesaj random pe general.', inline = False)
            embed.add_field(name = 'Comanda de help si modhelp', value = 'Lista comenzi pentru staff si membrii.', inline = False)
            embed.add_field(name = 'Fun', value = 'Hug/Kill/Kiss', inline = False)
            embed.add_field(name = 'Welcome/Leave System', value = 'Mesaje pe channel dedicat si joinul mai este anuntat si pe general.', inline = False)
            embed.add_field(name = 'Tag System', value = 'Primesti rol cand iti pui tagul in nume (exclus nick) si cand il scoti iti scoate si rolul.', inline = False)
            embed.add_field(name = '`ph?futures 2`', value = 'Next Page >>>', inline = False)
        elif page == 2:
            embed = Embed(color = 0xff006f, title = "Page 2 of futures")
            embed.set_footer(text = 'Made by iLectus#3916', icon_url='https://cdn.discordapp.com/attachments/768118506813390859/804786242692579348/phoenix_Logo2.png')
            embed.add_field(name = 'MarriageSystem', value = 'divorce/whomarried/marry', inline = False)
        else:
            embed = Embed(color = 0xff006f, title = "**Pagina asta nu exista**")
            embed.set_footer(text = 'Made by iLectus#3916', icon_url='https://cdn.discordapp.com/attachments/768118506813390859/804786242692579348/phoenix_Logo2.png')

        if 582267057194795018 == ctx.message.channel.id:
            await ctx.send(embed=embed, delete_after=60*5)
        else:
            await ctx.message.delete()
            await ctx.send(f"**{ctx.message.author.display_name}, scrie pe textchannel-ul potrivit!**", delete_after=5)

def setup(client):
    client.add_cog(Futures(client))