import discord
from discord.ext import commands
import yt_dlp
import os

# Configuração de permissões (Intents)
intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix='!', intents=intents)

# Configuração do buscador de música
YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'default_search': 'ytsearch',
    'nocheckcertificate': True,
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

@bot.event
async def on_ready():
    print(f'Annybot ligada e pronta para o {bot.user}!')

@bot.command()
async def play(ctx, *, search: str):
    if not ctx.author.voice:
        return await ctx.send("❌ Você precisa estar em um canal de voz!")
    
    if not ctx.voice_client:
        await ctx.author.voice.channel.connect()

    async with ctx.typing():
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info(f"ytsearch1:{search}", download=False)['entries'][0]
                url = info['url']
                source = await discord.FFmpegOpusAudio.from_probe(url, **FFMPEG_OPTIONS)
                
                if ctx.voice_client.is_playing():
                    ctx.voice_client.stop()
                    
                ctx.voice_client.play(source)
                await ctx.send(f"🎶 Tocando agora: **{info['title']}**")
            except Exception as e:
                await ctx.send("❌ Não consegui encontrar a música. Tente o nome completo!")

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Tchau! Saindo do canal.")

# Puxa o Token da variável do Railway
bot.run(os.getenv('DISCORD_TOKEN'))
