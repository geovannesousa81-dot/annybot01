import discord
from discord.ext import commands
import yt_dlp
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True  # ESSENCIAL PARA O !PLAY FUNCIONAR
bot = commands.Bot(command_prefix='!', intents=intents)

ytdl_format_options = {
    'format': 'bestaudio/best',
    'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}],
    'noplaylist': True,
}
ffmpeg_options = {'options': '-vn'}
ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

@bot.command(name='play')
async def play(ctx, *, search):
    if not ctx.author.voice:
        return await ctx.send("Você precisa estar em um canal de voz!")
    
    channel = ctx.author.voice.channel
    voice_client = ctx.voice_client if ctx.voice_client else await channel.connect()

    async with ctx.typing():
        info = ytdl.extract_info(f"ytsearch:{search}", download=False)['entries'][0]
        url = info['url']
        voice_client.play(discord.FFmpegPCMAudio(url, **ffmpeg_options))
    
    await ctx.send(f'🎶 Tocando agora: **{info["title"]}**')

@bot.event
async def on_ready():
    print(f'Bot {bot.user.name} está ONLINE e pronto para tocar!')

token = os.environ.get('DISCORD_TOKEN')
bot.run(token)
