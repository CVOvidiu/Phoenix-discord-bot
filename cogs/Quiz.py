import discord
import asyncio
from discord.ext import commands
from discord import Embed
from datetime import datetime

switch = 0

class Quiz(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def verify(self, ctx):
        global switch
        author = ctx.message.author
        
        await ctx.send("**Pentru a rezolva quiz-ul, uita-te in DM si raspunde la intrebari.**", delete_after = 3 * 60)
        await author.send("**Pentru a rezolva quiz-ul, raspunde la intrebarile urmatoare:**")

        q = [
            "**1. Baiat sau fata?**\n`1` pentru baiat\n`2` pentru fata",
            "**2. Cati ani ai?**\n`1` pentru -14\n`2` pentru 14-18\n`3` pentru 18+"
        ]


        for i in q:
            await author.send(i)

            try:
                message = await self.client.wait_for("message", check = lambda m: author == m.author and isinstance(m.channel, discord.DMChannel), timeout = 30.0)

            except asyncio.TimeoutError:
                await author.send("**Ti-a luat prea mult sa raspunzi... (30 secunde). Incearca din nou comanda!**")
                return
            else:
                if i[2] == '1':
                    fata = discord.utils.get(ctx.guild.roles, id = 571048442856734741)
                    baiat = discord.utils.get(ctx.guild.roles, id = 571048541523542042)
                    
                    if message.content == "2":
                        await author.add_roles(fata)
                        await author.remove_roles(baiat)
                        await author.send("**Raspuns :** *fata*")
                    elif message.content == "1":
                        await author.add_roles(baiat)
                        await author.remove_roles(fata)
                        await author.send("**Raspuns :** *baiat*")
                    else:
                        await author.send("**Raspunde cum trebuie! Incearca din nou comanda!**")
                        return

                if i[2] == '2':
                    one = discord.utils.get(ctx.guild.roles, id = 836942535216594964)
                    two = discord.utils.get(ctx.guild.roles, id = 836942902164717598)
                    three = discord.utils.get(ctx.guild.roles, id = 836942982968115230)

                    if message.content == "1":
                        await author.add_roles(one)
                        await author.remove_roles(two)
                        await author.remove_roles(three)
                        await author.send("**Raspuns :** *-14*")
                        switch = 1
                    elif message.content == "2":
                        await author.add_roles(two)
                        await author.remove_roles(one)
                        await author.remove_roles(three)
                        await author.send("**Raspuns :** *14-18*")
                        switch = 1
                    elif message.content == "3":
                        await author.add_roles(three)
                        await author.remove_roles(one)
                        await author.remove_roles(two)
                        await author.send("**Raspuns :** *18+*")
                        switch = 1
                    else:
                        await author.send("**Raspunde cum trebuie! Incearca din nou comanda!**")
                        return

        if switch == 1:
            member = discord.utils.get(ctx.guild.roles, id = 569096430514339852)
            not_ver = discord.utils.get(ctx.guild.roles, id = 878972176827551746)
            await author.send("**Quizul s-a sfarsit!**")
            await author.add_roles(member)
            await author.remove_roles(not_ver)

            reg = self.client.get_channel(569880437430812712) #Regulament mention
            tyr = self.client.get_channel(570616727952556032) #Take Your Roles mention
            info = self.client.get_channel(837687280931831849)
            channel = self.client.get_channel(569077625826443276) #General Chat

            header = f"""<:bfa_wow:885137445232967690> **Welcome,** {author.mention}
**Bine ai venit pe server!**
<@&884834209930313778>
            """
            await channel.send(header)
            description = f"""
            **╭┄┄┄┄┄ · ｡ﾟ･｡ﾟ･**
            **┊ ✦. :: {reg.mention} ｡ﾟ･ Regulament**
            **┊ ✦. :: {tyr.mention} ｡ﾟ･ Self Roles**
            **┊ ✦. :: {info.mention} ｡ﾟ･ Informatii**
            **┊ ✦. :: `ﾉʙꜰᴀ` ｡ﾟ･ Tag**
            **╰┄┄┄┄┄┄┄₊˚・｡ﾟ･**
            """
            embedJ = Embed(color = 0xe03a3e, description = description, timestamp = datetime.utcnow())
            embedJ.set_author(name = f'{author.display_name}#{author.discriminator}', icon_url = author.avatar_url)
            embedJ.set_footer(text = 'Thanks for joining!', icon_url = 'https://cdn.discordapp.com/attachments/768118506813390859/885141433667944489/hasjk.png')
            embedJ.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/768118506813390859/884854135042740224/Untitled-1.png')
            await channel.send(embed = embedJ)

    @verify.error
    async def verify_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("**Eroare :** *DM-urile sunt dezactivate. Incearca din nou comanda dupa ce le activezi.*")

def setup(client):
    client.add_cog(Quiz(client))