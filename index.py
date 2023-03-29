# Discord module 

import os
import asyncio
import subprocess
import shlex



import discord
from discord.ext import commands
from discord import User
from discord.ext.commands import MissingPermissions
from datetime import datetime
from async_timeout import timeout
import random 
import youtube_dl
import asyncio

# Prefix bot

intents = discord.Intents.all()
client = commands.Bot(command_prefix = "!", intents=intents)

# YoutubeDL !

@client.event
async def on_ready():
    print("Bot is live")
    await client.load_extension('playlist')
    for file in os.listdir("./Cogs"):
        if file.endswith(".py"):
            await client.load_extension(f'Cogs.{file[:-3]}')

# TODO: Refactor so that shell files can go into a folder
@client.command(name="reboot")
@commands.is_owner()
async def reboot(ctx):
    await ctx.send("Rebooting")
    subprocess.call(["sh", "./autorestart.sh"])


@client.command(name="backupPlaylists")
@commands.is_owner()
async def backup_playlists(ctx):
    await ctx.send("Backing up playlists and will send as a personal message.")
    if os.path.isfile('./backup.zip'):
        os.remove('./backup.zip')

    zipCommand = shlex.split("zip -r backup.zip ./Playlist")
    outcome = subprocess.Popen(zipCommand)
    waitCounter = 10
    while outcome.poll() is None and waitCounter > 0:
        await asyncio.sleep(1)
        waitCounter = waitCounter - 1

    if os.path.isfile('./backup.zip'):
        await ctx.author.send(file=discord.File(r'./backup.zip'))
        os.remove('./backup.zip')


# Bot event


@client.event
async def on_member_join(User):
   await client.get_channel(1090592726803816498).send(f"{User.name} has joined")

@client.event
async def on_member_remove(User):
   await client.get_channel(1090592937827631165).send(f"{User.name} has left")

@client.event
async def on_ready():
    print("START!")

# Administrator Command


@client.command()
async def about(ctx):
    print("About command")
    await about.send("UPMOON Alpha 0.1")
    
@client.command(aliases= ['purge','delete'])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount : int):
   if amount == None:
       await ctx.channel.purge(limit=1000000)
   else:
       await ctx.channel.purge(limit=amount)

@client.command()
async def ban(ctx, user : discord.User, *reason):
    reason = "".join(reason)
    await ctx.guild.ban(user, reason = reason)
    embed = discord.Embed(title = "**Banned**", description = " A moderator As ban ", color=0x691f0a)
    embed.set_thumbnail(url = "https://st2.depositphotos.com/2289871/5397/i/600/depositphotos_53975429-stock-photo-hand-in-jail.jpg")
    embed.add_field(name = "User Ban", value = user.name)
    embed.add_field(name ="Reason", value = reason)
    embed.add_field(name ="Person", value = ctx.author.name)

    await ctx.send(embed = embed)


@client.command()
async def kick(ctx, user : discord.User, *reason):
    reason ="".join(reason)
    await ctx.guild.kick(user, reason = reason)
    await ctx.send(f"{user} as ben kicked!")

@client.command()
async def changelog(ctx):
    print("Changelog command")
    head = "ChangeLOG"
    text1 = "NEW command : !changelog" 
    text2 = "New version number : 1.2RC Neptune Alpha!"
    text3 = "New prefix '!' "
    changelog = f"``` Welcome to {head}  \n{text2} \nNew of this Version {text1} and {text3} ```"
    embed = discord.Embed(title = f"**{head}**", description = f" \n{text1} \n{text2}\n{text3} ", color=0x691f0a)
    await ctx.send(embed = embed)

@client.command()
async def serverinfo(ctx):
    server = ctx.guild
    numberOfTextChannels = len(server.text_channels)
    numberOfVoiceChannels = len(server.voice_channels)
    serverdescription = server.description 
    NumberOfPerson = server.member_count
    serverName = server.name
    message = f"My server **{serverName}** have **{NumberOfPerson}** person. \nThe description of server **{serverdescription}**. \nThis server have **{numberOfTextChannels}** On Channel text and have **{numberOfVoiceChannels}** of Voice channel" 
    await ctx.send(message)

# Bot Token

client.run('MTA5MDE5NDA2MTIxNTkzNjU0Mg.GrbEwb.mvpf3BadTt4nOeIBCYxO0b-07WuOwUjvBE2sO4')