import discord
from discord.ext import commands, tasks
from discord import Embed, Emoji
from discord.ext.commands import BucketType, cooldown, CommandOnCooldown

class Modhelp(commands.Cog):
    def __init__(self, client):
        self.client = client

#embed.add_field(name = '', value = '', inline = False)

    @commands.command(aliases=['mh'])
    @cooldown(3, 60, BucketType.user)
    async def modhelp(self, ctx, page = 1):

        if page == 1:
            embed = Embed(title = '**Informatii Moderare**', description = 'Va multumim pentru ca ne sunteti alaturi. Pentru a lasa o sugestie in legatura cu BOT-ul, DM **iLectus** !', color = 0xe03a3e)
            embed.set_footer(text = 'Made by iLectus#3916', icon_url='https://cdn.discordapp.com/attachments/768118506813390859/804786242692579348/phoenix_Logo2.png')
            embed.add_field(name = '`ph?announce [mesaj]` <anno> - Announcement', value = 'Creeaza un anunt pe channelul de anunturi.', inline = False)
            embed.add_field(name = '`ph?clear [cate mesaje(default 10)]` - Stergere mesaje', value = 'Sterge mesajele de pe chat.', inline = False)
            embed.add_field(name = '`ph?kick [membrul] [motiv]` - Kick', value = 'Da un membru afara de pe server.', inline = False)
            embed.add_field(name = '`ph?ban [membrul] [motiv]` - Ban', value = 'Da ban unui membru de pe server.', inline = False)
            embed.add_field(name = '`ph?unban [membrul] [motiv]` - Unban', value = 'Pentru a da unban unui membru.', inline = False)
            embed.add_field(name = '`ph?mute [membrul] [timp(minute)] [motiv]` <m> - Mute', value = 'Pentru a da mute unui membru.', inline = False)
            embed.add_field(name = '`ph?unmute [membrul] [motiv]` <um> - Mute', value = 'Pentru a da unmute unui membru.', inline = False)
            embed.add_field(name = '`ph?parteneriat [link]` <p> - Parteneriat', value = 'Comanda de parteneriat.', inline = False)
            embed.add_field(name = '`ph?say [mesaj]` <s> - Spune', value = 'Vorbeste in numele botului.', inline = False)
            embed.add_field(name = '`ph?modhelp 2`', value = 'Next Page >>>', inline = False)
        elif page == 2:
            embed = Embed(color = 0xe03a3e, title = "Page 2 of modhelp")
            embed.set_footer(text = 'Made by iLectus#3916', icon_url='https://cdn.discordapp.com/attachments/768118506813390859/804786242692579348/phoenix_Logo2.png')
            embed.add_field(name = '`ph?embed [mesaj]` <e> - Embed', value = 'Trimite un embed in numele botului', inline = False)
            embed.add_field(name = '`ph?embedtitle [title(Fara spatii)] [mesaj]` <et> - EmbedTitle', value = 'Trimite un embed cu titlu in numele botului.', inline = False)
            embed.add_field(name = '`ph?take [credite] [membrul]` - Take credits (BOT OWNER)', value = 'Ia credite de la un membru.', inline = False)
            embed.add_field(name = '`ph?give [membrul] [credite]` - Give credits (BOT OWNER)', value = 'Dai unui membru credite.', inline = False)
            embed.add_field(name = '`ph?changebirthday [membrul] [zz/ll]` - Change birthday', value = 'Schimba ziua de nastere a unui membru.', inline = False)
        else:
            embed = Embed(color = 0xe03a3e, title = "**Pagina asta nu exista**")
            embed.set_footer(text = 'Made by iLectus#3916', icon_url='https://cdn.discordapp.com/attachments/768118506813390859/804786242692579348/phoenix_Logo2.png')

        if 582267057194795018 == ctx.message.channel.id:
            await ctx.send(embed=embed, delete_after=60*5)
        else:
            await ctx.message.delete()
            await ctx.send(f"**{ctx.message.author.display_name}, scrie pe textchannel-ul potrivit!**", delete_after=5)

    @modhelp.error
    async def modhelp_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            await ctx.message.delete()
            embed = Embed(description=f'Command on cooldown, try again in {error.retry_after:,.2f} seconds.', color=0xff0004)
            await ctx.send(embed=embed, delete_after=5)

def setup(client):
    client.add_cog(Modhelp(client))
