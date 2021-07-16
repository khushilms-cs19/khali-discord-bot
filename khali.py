import os
import discord
from discord import colour
from discord import guild
from discord.ext import commands
import random
import asyncpraw

import json
import youtube_dl
from dotenv import load_dotenv
load_dotenv()

TOKEN=os.getenv("DISCORD_TOKEN")
PASSWORD=os.getenv("PASSWORD")
USERNAME=os.getenv("ID_USERNAME")
CLIENT_ID=os.getenv("CLIENT_ID")
CLIENT_SECRET=os.getenv("CLIENT_SECRET")

reddit=asyncpraw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    password=PASSWORD,
    username=USERNAME,
    user_agent="Khali bhai se panga nahi, samjha kya"
)

async def get_meme():
    subreddit=await reddit.subreddit("meme")
    all_subs=[]
    top=subreddit.top(limit=100)
    async for submissions in top:
        all_subs.append(submissions)
    random_sub=random.choice(all_subs)
    return random_sub

description="Hello Guys WhatApp?? Bonky Bonk here"
intents=discord.Intents.default()

bot=commands.Bot(command_prefix="^",description=description,intents=intents)


@bot.event
async def on_ready():
    print("Bot is running")
    game=discord.Game("with your mum XD")
    await bot.change_presence(status=discord.Status.do_not_disturb,activity=game)


@bot.command()
async def add(ctx,a : int,b : int):
    msg=f"Saale itta bhi nahi aata BC!! ye le: \n{a} + {b} = {a+b}"
    await ctx.send(msg)

@bot.command()
async def choose(ctx,*choices):
    msg="Ye le : "+str(random.choice(choices))
    await ctx.send(msg)

@bot.command()
async def memede(ctx):
    meme=await get_meme()
    name=ctx.message.author
    url=meme.url
    embed=discord.Embed(title=f"__{str(name)[:-5]} ye le tera meme, funny ke chode__",color=discord.Color.random(),timestamp=ctx.message.created_at,url=url)
    embed.set_author(name=ctx.message.author,icon_url=ctx.author.avatar_url)
    embed.set_image(url=url)
    embed.set_footer(text=f"{meme.title}")
    await ctx.send(embed=embed)

@bot.command()
async def play(ctx,*query: str):
    query=" ".join(query)
    try: 
        voiceChannel=ctx.message.author.voice.channel
    except:
        await ctx.send("Pehle voice channel join kar mere bhai🙏")
        return    
    voice=discord.utils.get(bot.voice_clients,guild=ctx.guild)

    def makeEmbed(title,url):
        embed=discord.Embed(title="Now Playing", colour=discord.Color.random())
        embed.add_field(name='song',value=title)
        embed.set_image(url=url)
        return embed

    if(voice==None):
        voice= await voiceChannel.connect()
        with youtube_dl.YoutubeDL({}) as ydl:
            song=ydl.extract_info(f'ytsearch:{query}',download=False)
            voice.play(discord.FFmpegPCMAudio("khalivoice.mp3"))
            voice.stop()
            print(song['entries'][0]['formats'][0]['url'])
            voice.play(discord.FFmpegPCMAudio(song['entries'][0]['formats'][0]['url']))
            await ctx.send(f"now playing: {song['entries'][0]['title']}")
    elif voice.is_connected:
        with youtube_dl.YoutubeDL({}) as ydl:
            song=ydl.extract_info(f'ytsearch:{query}',download=False)
            voice.stop()
            print(song['entries'][0]['formats'][0]['url'])
            voice.play(discord.FFmpegPCMAudio(song['entries'][0]['formats'][0]['url']))
            await ctx.send(f"now playing: {song['entries'][0]['title']}")
@bot.command()
async def stop(ctx):
    try: 
        voice=discord.utils.get(bot.voice_clients,guild=ctx.message.guild)
        if voice.is_connected:
            voice.stop()
            await ctx.send("Haa bhai okay gand much ke baithta hu!! -_-")
        else:
            await ctx.send("Pehle voice channel ko connect kar chutiye")
    except:
        await ctx.send("Pehle voice channel me connect kar chutiye")        

@bot.command()
async def pause(ctx):
    try: 
        voice=discord.utils.get(bot.voice_clients,guild=ctx.message.guild)
        if voice.is_connected:
            voice.pause()
            await ctx.send("Haa rukta hu thodi der ^_^. Song Paused!!")
        else:
            await ctx.send("Pehle voice channel me connect kar chutiye")    
    except:
        await ctx.send("Pehle voice channel me connect kar chutiye")        

@bot.command()
async def resume(ctx):
    try: 
        voice=discord.utils.get(bot.voice_clients,guild=ctx.message.guild)
        if voice.is_connected:
            voice.resume()
            await ctx.send("Resumed Song")
        else:
            await ctx.send("Pehle voice channel me connect kar chutiye")
    except:
        await ctx.send("Pehle voice channel me connect kar chutiye")        


@bot.command()
async def disconnect(ctx):
    try:
        voice=discord.utils.get(bot.voice_clients,guild=ctx.message.guild)
        if voice.is_connected:
            await voice.disconnect()
            await ctx.send("thike hai bhai abb me chalta hu")
        else:
            await ctx.send("Pehle voice channel me connect kar chutiye")
    except:
        await ctx.send("Pehle voice channel me connect kar chutiye")

@bot.command()
async def aaja(ctx):
    try: 
        voiceChannel=ctx.message.author.voice.channel
    except:
        await ctx.send("Pehle voice channel join kar mere bhai🙏")
        return
    voice =await voiceChannel.connect()    
    voice.play(discord.FFmpegPCMAudio("khalivoice.mp3"))

@bot.command()
async def love(ctx):
    embed=discord.Embed(title="I Love You💕",colour=discord.Color.random(),timestamp=ctx.message.created_at)
    embed.set_author(name=ctx.message.author,icon_url=ctx.author.avatar_url)
    embed.set_image(url="""https://simg-memechat.s3.ap-south-1.amazonaws.com/EnBnQ1QORjbeKH068z22mYWE6KFfl7368946.jpg""")
    embed.set_footer(text=f"Dont worry when im there")
    await ctx.send(embed=embed)

bot.run(TOKEN)