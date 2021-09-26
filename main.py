import yaml
import os
import discord
from discord.ext import commands 
from music import newmusic

f = open("config.yml", "r")
cfg = yaml.load(f, Loader=yaml.FullLoader)

configMessages = cfg["messages"]
configMain = cfg["main"]

intents = discord.Intents().all()
client = commands.Bot(command_prefix='!', intents = intents)

@client.event
async def on_ready():
    print('Music.bot ready')
    print(configMain["discord_token"])

async def setup():
    await client.wait_until_ready() 
    client.add_cog(newmusic(client))



client.loop.create_task(setup())
client.run(configMain["discord_token"])
