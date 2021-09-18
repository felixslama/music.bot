import discord
from discord.ext import commands
import music

cogs = [music]
intents = discord.Intents().all()
client = commands.Bot(command_prefix='!', intents = intents)
for i in range(len(cogs)):
    cogs[i].setup(client)

client.run("ODc0NzI4ODI1MTY1MDYyMTk0.YRLMsw.tXKUf5DWO_ZdnDaaNnRdrXYvSQc")