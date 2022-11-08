import discord
from discord.ext import commands
from discord import Embed

#TODO: Integrare in baza de date (RunningEventsPerUser)
'''
- Adaugam in baza fiecarui user numarul de banuri date intr-un inteval de timp
- Daca depaseste intervalul > Quarantine + remove Mod + stergem din baza numarul de banuri stranse
- Daca nu depaseste intervalul, dupa ce trece intervalul stergem din baza numarul de banuri stranse
'''

class Ban(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member : discord.Member, *, reason = None):
        staff = discord.utils.get(ctx.guild.roles, id = 876759046336688138)
        if member.id == ctx.author.id:
            await ctx.send(embed = Embed(color = 0xe03a3e, description = f":white_circle: **{ctx.message.author.display_name}, iti da ban Lectus, daca tot vrei. |** :white_check_mark:"))
        elif staff in member.roles:
            await ctx.send(embed = Embed(color = 0xe03a3e, description = f":white_circle: **{ctx.message.author.display_name}, nu poti da ban unui membru staff! |** :white_check_mark:"))
        else:
            punishroom = self.client.get_channel(583619328625344512)
            await member.send(embed = Embed(color = 0xe03a3e, title = f":white_circle: **Ai fost banat pe server. |** :no_entry:", description="**Motiv: **" + str(reason)))
            await member.ban(reason = reason)
            await ctx.send(embed = Embed(color = 0xe03a3e , description = f":white_circle: **{ctx.message.author.display_name}, ai banat membrul {member.mention}. |** :white_check_mark:"))
            await punishroom.send(embed = Embed(color = 0xe03a3e, title = f":white_circle: **Membrul {member} a fost banat de catre {ctx.message.author.display_name}. |** :white_check_mark:", description = "**Motiv: **" + str(reason)))

    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def unban(self, ctx, member_id : str, *, reason = None):
        switch = 0
        banned_users = await ctx.guild.bans()
        for ban_entry in banned_users:
            user = ban_entry.user
            if str(user.id) == member_id:
                switch = 1
                punishroom = self.client.get_channel(583619328625344512)
                await ctx.guild.unban(user, reason = reason)
                await ctx.send(embed = Embed(color = 0xe03a3e, description = f":white_circle: **{ctx.message.author.display_name}, ai dat unban userului {user.display_name}#{user.discriminator}. |** :white_check_mark:"))
                await punishroom.send(embed = Embed(color = 0xe03a3e, title = f":white_circle: **Userul {user.display_name}#{user.discriminator} a fost debanat de catre {ctx.message.author.display_name}. |** :white_check_mark:", description = "**Motiv: **" + str(reason)))
                return # Odata ce l-a gasit, sa nu mai continue loopul
        if switch == 0:
            await ctx.send(embed = Embed(color = 0xe03a3e, description = f":white_circle: **{ctx.message.author.display_name}, nu am gasit niciun membru cu id-ul `{member_id}`. Sigur ai scris comanda corect? :** `ph?unban <ID> <Motiv>` **|** :grey_question:", delete_after = 60))

    # Error Management :
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = Embed(color = 0xe03a3e, description = f":white_circle: **{ctx.message.author.display_name}, nu ai permisiunea de a bana acest membru. |** :no_entry:", delete_after = 60)
            await ctx.send(embed = embed)
        if isinstance(error, commands.MissingRequiredArgument):
            embed = Embed(color = 0xe03a3e, description = f":white_circle: **{ctx.message.author.display_name}, ceva nu e bine... :** `ph?ban <Membru> <Motiv>` **|** :grey_question:", delete_after = 60)
            await ctx.send(embed = embed)
        if isinstance(error, commands.MemberNotFound):
            embed = Embed(color = 0xe03a3e, description = f":white_circle: **{ctx.message.author.display_name}, ceva nu e bine... :** `ph?ban <Membru> <Motiv>` **|** :grey_question:", delete_after = 60)
            await ctx.send(embed = embed)

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = Embed(color = 0xe03a3e, description = f":white_circle: **{ctx.message.author.display_name}, nu ai permisiunea de a debana acest membru. |** :no_entry:", delete_after = 60)
            await ctx.send(embed = embed)
        if isinstance(error, commands.MissingRequiredArgument):
            embed = Embed(color = 0xe03a3e, description = f":white_circle: **{ctx.message.author.display_name}, ceva nu e bine... :** `ph?unban <ID> <Motiv>` **|** :grey_question:", delete_after = 60)
            await ctx.send(embed = embed)

def setup(client):
    client.add_cog(Ban(client))
