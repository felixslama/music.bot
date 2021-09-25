import os
import discord
from discord.ext import commands 
from music import newmusic

intents = discord.Intents().all()
client = commands.Bot(command_prefix='!', intents = intents)

@client.event
async def on_ready():
    print('Music.bot ready')

async def setup():
    await client.wait_until_ready() 
    client.add_cog(newmusic(client))

client.loop.create_task(setup())
client.run("ODc0NzI4ODI1MTY1MDYyMTk0.YRLMsw.tXKUf5DWO_ZdnDaaNnRdrXYvSQc")
