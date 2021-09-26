import yaml
import asyncio
import discord
import pafy
from discord.ext import commands
import youtube_dl

f = open("config.yml", "r")
cfg = yaml.load(f, Loader=yaml.FullLoader)

configMessages = cfg["messages"]
configMain = cfg["main"]

class newmusic(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.queue = {}
        self.setup()
    def setup(self):
        for g in self.client.guilds:
            self.queue[g.id] = []

    @commands.command()
    async def join(self,ctx):
        if ctx.author.voice is None:
            embed = discord.Embed(title="Music.BOT",url="https://github.com/felixslama/music.bot", description=configMessages["notInVoice"],color=configMessages["embedColor"]())
            await ctx.send(embed=embed)
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        elif ctx.voice_client.channel != ctx.author.voice.channel:
            embed = discord.Embed(title="Music.BOT",url="https://github.com/felixslama/music.bot", description=configMessages["alreadyInUse"],color=configMessages["embedColor"]())
            await ctx.send(embed=embed)

    async def checkqueue(self,ctx):
        if len(self.queue[ctx.guild.id]) > 0:
            ctx.voice_client.stop()
            await self.playsong(ctx,self.queue[ctx.guild.id][0])
            self.queue[ctx.guild.id].pop(0)
    async def searchurl(self,amount,song,get_url=False):
        info = await self.client.loop.run_in_executor(None, lambda:youtube_dl.YoutubeDL({'format':"bestaudio","quiet": True}).extract_info(f"ytsearch{amount}:{song}", download=False, ie_key="YoutubeSearch"))
        if len(info["entries"]) == 0: return None

        return[entry["webpage_url"] for entry in info["entries" if get_url else info]]

    async def playsong(self,ctx,song):
        url = pafy.new(song).getbestaudio().url
        ctx.voice_client.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(url)), after=lambda error: self.client.loop.create_task(self.checkqueue(ctx)))
        ctx.voice_client.source.volume = 0.5

    @commands.command()
    async def play(self, ctx, *,song=None):
        if song is None:
            embed = discord.Embed(title="Music.BOT",url="https://github.com/felixslama/music.bot", description=configMessages["noLink"],color=configMessages["embedColor"]())
            return await ctx.send(embed=embed)

        if ctx.author.voice is None:
            embed = discord.Embed(title="Music.BOT",url="https://github.com/felixslama/music.bot", description=configMessages["notInVoice"],color=configMessages["embedColor"]())
            return await ctx.send(embed=embed)

        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect()
        elif ctx.voice_client.channel != ctx.author.voice.channel:
            embed = discord.Embed(title="Music.BOT",url="https://github.com/felixslama/music.bot", description=configMessages["alreadyInUse"],color=configMessages["embedColor"]())
            return await ctx.send(embed=embed)

        if not("youtube.com/watch?" in song or "https://youtu.be" in song):
            await ctx.send("Link not known. Starting search")
            result = await self.searchurl(1, song,get_url=True)
            if result is None:
                embed = discord.Embed(title="Music.BOT",url="https://github.com/felixslama/music.bot", description=configMessages["searchNoResults"],color=configMessages["embedColor"]())
                return await ctx.send(embed=embed)
            song = result[0]
        if ctx.voice_client.source is not None:
            queue_len = len(self.queue[ctx.guild.id])

            if queue_len < 20:
                self.queue[ctx.guild.id].append(song)
                embed = discord.Embed(title="Music.BOT",url="https://github.com/felixslama/music.bot", description=configMessages["addedToQueue"].format(queue_len=queue_len+1),color=configMessages["embedColor"]())
                return await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="Music.BOT",url="https://github.com/felixslama/music.bot", description=configMessages["queueIsFull"],color=configMessages["embedColor"]())
                return await ctx.send(embed=embed)
        await self.playsong(ctx,song)
        embed = discord.Embed(title="Music.BOT",url="https://github.com/felixslama/music.bot", description=configMessages["nowPlaying"].format(song=song),color=configMessages["embedColor"]())
        await ctx.send(embed=embed)

    @commands.command()
    async def skip(self, ctx):
        if ctx.author.voice is None:
            embed = discord.Embed(title="Music.BOT",url="https://github.com/felixslama/music.bot", description=configMessages["notInVoice"],color=configMessages["embedColor"]())
            await ctx.send(embed=embed)

        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect()
        elif ctx.voice_client.channel != ctx.author.voice.channel:
            embed = discord.Embed(title="Music.BOT",url="https://github.com/felixslama/music.bot", description=configMessages["alreadyInUse"],color=configMessages["embedColor"]())
            await ctx.send(embed=embed)
        
        ctx.voice_client.stop()
        embed = discord.Embed(title="Music.BOT",url="https://github.com/felixslama/music.bot", description=configMessages["skip"],color=configMessages["embedColor"]())
        await ctx.send(embed=embed)
        await self.checkqueue(ctx)
    
    @commands.command()
    async def pause(self,ctx):
        embed = discord.Embed(title="Music.BOT",url="https://github.com/felixslama/music.bot", description=configMessages["paused"],color=configMessages["embedColor"]())
        await ctx.send(embed=embed)
        await ctx.voice_client.pause()
        
    
    @commands.command()
    async def resume(self,ctx):
        embed = discord.Embed(title="Music.BOT",url="https://github.com/felixslama/music.bot", description=configMessages["resumed"],color=configMessages["embedColor"]())
        await ctx.send(embed=embed)
        await ctx.voice_client.resume()

    @commands.command()
    async def info(self,ctx):
        embed = discord.Embed(title="Music.BOT",url="https://github.com/felixslama/music.bot", description=configMessages["infoMsg"],color=configMessages["embedColor"]())
        await ctx.send(embed=embed)

    @commands.command()
    async def stop(self,ctx):
        ctx.voice_client.stop()
        self.queue[ctx.guild.id].clear()
        embed = discord.Embed(title="Music.BOT",url="https://github.com/felixslama/music.bot", description=configMessages["clear"],color=configMessages["embedColor"]())
        await ctx.send(embed=embed)
    async def clear(self,ctx):
        ctx.voice_client.stop()
        self.queue[ctx.guild.id].clear()
        embed = discord.Embed(title="Music.BOT",url="https://github.com/felixslama/music.bot", description=configMessages["stop"],color=configMessages["embedColor"]())
        await ctx.send(embed=embed)

    @commands.command()
    async def next(self, ctx):
        if ctx.author.voice is None:
            embed = discord.Embed(title="Music.BOT",url="https://github.com/felixslama/music.bot", description=configMessages["notInVoice"],color=configMessages["embedColor"]())
            await ctx.send(embed=embed)

        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect()
        elif ctx.voice_client.channel != ctx.author.voice.channel:
            embed = discord.Embed(title="Music.BOT",url="https://github.com/felixslama/music.bot", description=configMessages["alreadyInUse"],color=configMessages["embedColor"]())
            await ctx.send(embed=embed)
        
        ctx.voice_client.stop()
        embed = discord.Embed(title="Music.BOT",url="https://github.com/felixslama/music.bot", description=configMessages["skip"],color=configMessages["embedColor"]())
        await ctx.send(embed=embed)
        await self.checkqueue(ctx)