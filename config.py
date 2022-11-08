#-------------------------------------------------------------------------------------------------------#
#                                                                                                       #
# __________                   __               __    __________.__                         .__         #
# \______   \_______  ____    |__| ____   _____/  |_  \______   \  |__   ____   ____   ____ |__|__  ___ #
#  |     ___/\_  __ \/  _ \   |  |/ __ \_/ ___\   __\  |     ___/  |  \ /  _ \_/ __ \ /    \|  \  \/  / #
#  |    |     |  | \(  <_> )  |  \  ___/\  \___|  |    |    |   |   Y  (  <_> )  ___/|   |  \  |>    <  #
#  |____|     |__|   \____/\__|  |\___  >\___  >__|    |____|   |___|  /\____/ \___  >___|  /__/__/\_ \ #
#                        \______|    \/     \/                      \/            \/     \/         \/  #
#                                                                                    -by iLectus#3916   #
#-------------------------------------------------------------------------------------------------------#

import discord
import os
from discord.ext import commands

intents = discord.Intents()
client = commands.Bot(command_prefix = 'ph?', intents = intents.all())

token = '' # Token removed
client.remove_command('help')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(token)
