import discord
from discord.ext import commands
from discord.ext.commands import bot
from discord import utils
from discord import Streaming
import requests
import io
import os
import aiohttp
import requests
import requests
import asyncio

PREFIX='.'
client = commands.Bot(command_prefix=PREFIX) 
client.remove_command('help')

EXCROLES=()
MAX_ROLES_PER_USER=5
#check
@client.event
async def on_ready():
    print("Бот работает.")
    client.loop.create_task(checkmem())
async def checkmem():
    while not client.is_closed():
        guild = client.get_guild(521030397157441536)
        mem = [m for m in guild.members if not m.bot]
        offline = len([1 for i in mem if str(i.status) in ['offline', 'invisible']])
        await client.get_channel(728363209240739844).edit(name=f"🔵Своих→ {len(mem)}")
        await client.get_channel(739465793355644988).edit(name=f"В онлайн : {len(mem) - offline}")
        b = 0
        channel = client.get_channel(739464885879963678)
        for i in guild.voice_channels:
            b += len(i.members)
        await channel.edit(name = f"В voice : {b}")

voiceID = 737311951348039743
channels = {} 

@client.event
async def on_voice_state_update(member:discord.Member, before, after):
    if before.channel and before.channel.id in channels.keys() and len(before.channel.members) == 0:
        temp = channels.pop(before.channel.id)
        await temp['voice'].delete()
        await temp['text'].delete()
        await temp['cat'].delete()

    if(after.channel and after.channel.id == voiceID):
        category= await member.guild.create_category_channel(name=f"👥Комната {member.name}")
        voiceChannel= await member.guild.create_voice_channel(f"👥 ┇ {member.name}", overwrites={
            member: discord.PermissionOverwrite(
                connect=True, speak=True, move_members=True, manage_channels=True, manage_roles=True, use_voice_activation=True)
        }, category=category, reason="Голосовая комната.")
        textChannel =await member.guild.create_text_channel(f"👥 ┇ {member.name}", overwrites={
            member: discord.PermissionOverwrite(
                connect=True, speak=True, move_members=True, manage_channels=True, manage_roles=True, use_voice_activation=True)
        }, category=category, reason="Текстовая комната.")
        await member.move_to(voiceChannel, reason="Перенос участника в его голосовую комнату.")
        for channel in client.get_channel(voiceID).category.voice_channels:
            if(channel.id == voiceID or len(channel.members) != 0): continue
            await channel.delete(reason="В голосовой комнате 0 людей!")
            await voiceChannel.delete()
            await textChannel.delete()

        channels.update({voiceChannel.id: {'voice' : voiceChannel, 'text' : textChannel, 'cat' : category}})
@client.command()
@commands.has_permissions(administrator=True)
async def ping(ctx):
    await ctx.send(f'Пинг: {client.latency}!')



#shit 
@client.command(pass_context=True)
@commands.has_any_role(550707413058191375,530159744594477066)
async def grant(ctx,member:discord.Member,Role:discord.Role,time:int):
    emb = discord.Embed(description=f':white_check_mark: Была выдана роль!',colour=discord.Color.green())
    if time == 0:
        await member.add_roles(Role)
        await ctx.send(embed=emb)
    else:
        await member.add_roles(Role)
        await ctx.send(embed=emb)
        await asyncio.sleep(time*60)
        await member.remove_roles(Role)
@client.command(pass_context=True)
@commands.has_any_role(550707413058191375,530159744594477066)
async def ungrant(ctx,member:discord.Member,Role:discord.Role):
    emb = discord.Embed(description=f':white_check_mark: Была убрана роль!',colour=discord.Color.green())
    await member.remove_roles(Role)
    await ctx.send(embed=emb)
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def say(ctx, *,message):
    channel = client.get_channel(736826404523606029,530159744594477066)
    emb = discord.Embed(title='СВОИ',description=f'{message}',colour=discord.Color.blue())
    emb.set_thumbnail(url="https://media.discordapp.net/attachments/679123068685385729/679123366527107072/def719137c3f6be9.gif?width=499&height=499")
    emb.set_footer(text=ctx.author.name,icon_url=ctx.author.avatar_url)
    await ctx.channel.purge(limit=1)
    await channel.send(message)
@client.command()
async def server(ctx):
    mem = [m for m in ctx.guild.members if not m.bot]
    offline = len([1 for i in mem if str(i.status) in ['offline', 'invisible']])
    emb = discord.Embed(title='Участники', colour=discord.Color.blue())
    emb.add_field(name=':grinning: Участников:', value=f'{len(mem)}', inline=True)
    emb.add_field(name=':white_check_mark: Онлайн:', value=f'{len(mem) - offline}', inline=True)
    emb.add_field(name=':x: Оффлайн:', value=f'{offline}', inline=True)
    emb.set_footer(text=ctx.author.name,icon_url=ctx.author.avatar_url)
    await ctx.send(embed=emb)




            



    


client.run('NzM5NDU4NDIyODAxNDMyNjI2.XyawUg.Amh1bHoUncMWOxxk7Vel5D46F6s')
