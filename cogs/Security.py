import discord
from discord import utils
from discord.enums import AuditLogAction
from discord.ext import commands
from discord import Embed

class Security(commands.Cog):
    def __init__(self, client):
        self.client = client

    '''
    Integrated Security in:
    - Bans - TODO
    '''

    '''Restrict Click-Ban'''
    @commands.Cog.listener()
    async def on_member_ban(self, guild, member):
        logs_chan = guild.get_channel(877659413643657276)
        quarantine = discord.utils.get(guild.roles, id = 842010066629689345)
        mod = discord.utils.get(guild.roles, id = 791459807747506226)
        logs = await guild.audit_logs(limit = 1, action = AuditLogAction.ban).flatten()
        logs = logs[0]
        if logs.target == member:
            await logs.user.add_roles(quarantine)
            await logs.user.remove_roles(mod)
            await logs_chan.send(embed = Embed(description = f"<a:blk_heart:877666480718762026> | {logs.user} was quarantined. (Click-Banned)"))

def setup(client):
    client.add_cog(Security(client))