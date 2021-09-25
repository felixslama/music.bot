import asyncio
import discord
import pafy
from discord.ext import commands
import youtube_dl


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
            await ctx.send("You need to be in a voice channel to use me!")
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        elif ctx.voice_client.channel != ctx.author.voice.channel:
            await ctx.send("I am already being used!")

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
            return await ctx.send("I need a link to play stuff")

        if ctx.author.voice is None:
            await ctx.send("You need to be in a voice channel to use me!")

        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect()
        elif ctx.voice_client.channel != ctx.author.voice.channel:
            await ctx.send("I am already being used!")

        if not("youtube.com/watch?" in song or "https://youtu.be" in song):
            await ctx.send("Link not known. Starting search")
            result = await self.searchurl(1, song,get_url=True)
            if result is None:
                return await ctx.send("Sorry, nothing found")
            song = result[0]
        if ctx.voice_client.source is not None:
            queue_len = len(self.queue[ctx.guild.id])

            if queue_len < 20:
                self.queue[ctx.guild.id].append(song)
                return await ctx.send(f"Song added! {queue_len +1} songs in queue")
            else:
                return await ctx.send("Queue is full.")
        await self.playsong(ctx,song)
        await ctx.send(f"Now playing: {song}")

    @commands.command()
    async def skip(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("You need to be in a voice channel to use me!")

        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect()
        elif ctx.voice_client.channel != ctx.author.voice.channel:
            await ctx.send("I am already being used!")
        
        ctx.voice_client.stop()
        await self.checkqueue(ctx)