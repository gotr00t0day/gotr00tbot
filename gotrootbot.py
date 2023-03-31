import discord,os,socket
import subprocess
import random 
import asyncio
import string
import hashlib
import socket
import requests
import http.client
import dns.resolver
import time
import whois
from convertion import convertmin, converthr, convertdays
from datetime import datetime
from translate import Translator
from builtwith import builtwith
from urllib.parse import urlencode
from discord.ext.commands import Bot
from discord.ext import commands
from googlesearch import search
from fake_useragent import UserAgent

token = ""

intents = discord.Intents.default()

intents.members = True
intents.message_content = True
intents.presences = True

client = commands.Bot(command_prefix='.', intents=intents)

client.remove_command('help')



# AUTHOR (c0deNinja - gotr00tbot v1.1)

@client.command(name="author")
async def _author(ctx):
        embed = discord.Embed(
            title = 'c0deNinja', 
            description='', 
            colour = discord.Colour.blue()
        )
        embed.set_footer(text='Developer, Programmer, Hacker')
        file = discord.File("img/hacker.jpg", filename="hacker.jpg")
        embed.set_image(url='attachment://hacker.jpg')
        await ctx.send(file=file, embed=embed)



############ STAFF COMMAND CENTER #################


# KICK

@client.command()
@commands.has_any_role("Admin", "Mods")
async def kick(ctx, member : discord.Member):
    try:
        await member.kick()
        await ctx.message.delete()
        embed=discord.Embed(title="User Kicked!", description="**{0}** was kicked by **{1}**!".format(member, ctx.message.author), colour=discord.Colour.blue())
        await ctx.send(embed=embed)
    except discord.ext.commands.errors.CommandInvokeError:
        await ctx.send("YOU DONT HAVE PERMISSION TO USE THIS COMMAND")

# BAN

@client.command()
@commands.has_any_role("Admin", "Mods")
async def ban(ctx, member : discord.Member, duration, *, arg):
    try:
        await member.ban(arg)
        await ctx.message.delete()
        embed=discord.Embed(title="User Banned!", description="**{0}** was banned by **{1}**! Reason: **{2}**".format(member, ctx.message.author, arg), colour=discord.Colour.blue())
        await ctx.send(embed=embed)
        await member.send(embed=embed)
        if "m" in duration:
            duration = duration.replace("m", "")
            await asyncio.sleep(convertmin(int(duration)))
        elif "h" in duration:
            duration = duration.replace("h", "")
            await asyncio.sleep(converthr(int(duration)))
        elif "d" in duration:
            duration = duration.replace("d", "")
            await asyncio.sleep(convertdays(int(duration)))
    except discord.ext.commands.errors.CommandInvokeError:
        await ctx.send("YOU DONT HAVE PERSMISSION TO USE THIS COMMAND")

# MUTE

@client.command()
@commands.has_any_role("Admin", "Mods")
async def mute(ctx, member : discord.Member, duration, *, arg):
    role = discord.utils.get(member.guild.roles, name='Muted')
    await member.add_roles(role)
    await ctx.message.delete()
    embed=discord.Embed(title="User Muted!", description="**{0}** was muted by **{1}**! Reason: **{2}**".format(member, ctx.message.author, arg), colour=discord.Colour.blue())
    await ctx.send(embed=embed)
    await member.send(embed=embed)
    if "m" in duration:
        duration = duration.replace("m", "")
        await asyncio.sleep(convertmin(int(duration)))
        await member.remove_roles(role)
    elif "h" in duration:
        duration = duration.replace("h", "")
        await asyncio.sleep(converthr(int(duration)))
        await member.remove_roles(role)
    elif "d" in duration:
        duration = duration.replace("d", "")
        await asyncio.sleep(convertdays(int(duration)))    
        await member.remove_roles(role)

# TEMPBAN

@client.command(name='tban')
@commands.has_any_role("Admin", "Mods")
async def _tban(ctx, member : discord.Member, duration, *, arg):
    role = discord.utils.get(member.guild.roles, name="TempBan")
    await member.add_roles(role)
    await ctx.message.delete()
    embed=discord.Embed(title="User banned temporary!", description="**{0}** was temp banned by **{1}**! Reason: **{2}**".format(member, ctx.message.author, arg), colour=discord.Colour.blue())
    await ctx.send(embed=embed)
    await member.send(embed=embed)
    if "m" in duration:
        duration = duration.replace("m", "")
        await asyncio.sleep(convertmin(int(duration)))
        await member.remove_roles(role)
    elif "h" in duration:
        duration = duration.replace("h", "")
        await asyncio.sleep(converthr(int(duration)))
        await member.remove_roles(role)
    elif "d" in duration:
        duration = duration.replace("d", "")
        await asyncio.sleep(convertdays(int(duration)))
        await member.remove_roles(role)


# UNBAN

@client.command(name='unban')
@commands.has_any_role("Admin", "Mods")
async def _unban(ctx, member : discord.Member):
    role = discord.utils.get(member.guild.roles, name="TempBan")
    await member.unban()
    await ctx.message.delete()
    await member.remove_roles(role)
    embed=discord.Embed(title="User unbanned!", description="**{0}** was unbanned by **{1}**!".format(member, ctx.message.author), colour=discord.Colour.blue())
    await ctx.send(embed=embed)


# SLOWMODE

@client.command(name="slowmode")
async def _lockdown(ctx, *, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    if seconds == 0:
        await ctx.send("slowmode **off**")
    else:
        await ctx.send(f"slowmode started for {seconds} seconds!")


# GET ALL CHANNELS

@client.command(name="channels")
async def _allchannels(ctx):
    chans = []
    for guild in client.guilds:
        for channel in guild.text_channels:
            chans.append(channel)
    for i in chans:
        channels = i
    await ctx.send(f"Channels: {len(guild.text_channels)}")

########################################################





##################### HANDLE ERRORS ################################

@kick.error
async def info_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('I could not find that member...')


######################################################################





# LIST ALL MODS

@client.command(name='mods')
async def _mods(ctx):
    mods = []
    for member in client.get_all_members():
        for role in member.roles:
            if role.name == "Mods":
                mods.append(str(member))
    moderators = [i.split('#', 1)[0] for i in mods]
    embed = discord.Embed(colour = discord.Colour.blue())
    file = discord.File("img/mods.png", filename="mods.png")
    embed.set_thumbnail(url='attachment://mods.png')
    embed.add_field(name='Mods', value="▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬", inline=False)
    embed.add_field(name='Mod', value=moderators[0], inline=True)
    embed.add_field(name='Mod', value=moderators[1], inline=True)
    embed.add_field(name='Mod', value=moderators[2], inline=True)
    embed.add_field(name='Mod', value=moderators[3], inline=True)
    embed.add_field(name='Mod', value=moderators[4], inline=True)
    embed.add_field(name='Mod', value=moderators[5], inline=True)
    embed.add_field(name='Mod', value=moderators[6], inline=True)
    await ctx.send(file=file, embed=embed)

# LIST ALL ADMINS


@client.command(name='admins')
async def _admins(ctx):
    admins = []
    for member in client.get_all_members():
        for role in member.roles:
            if role.name == "Admin":
                admins.append(str(member))
    adminslist = [i.split('#', 1)[0] for i in admins]
    embed = discord.Embed(colour = discord.Colour.blue())
    embed.add_field(name='Admins', value="▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬", inline=False)
    embed.add_field(name='Admin', value=adminslist[0], inline=False)
    embed.add_field(name='Admin', value=adminslist[1], inline=False)
    embed.add_field(name='Admin', value=adminslist[2], inline=False)
    await ctx.send(embed=embed)



# ONLINE

@client.command(name='onlinecheck')
async def _checkuser(ctx, *, arg: discord.User):
    online = []
    for guild in client.guilds:
        for member in guild.members:
            if str(member.status) != "offline":
                online.append(f"{str(member)}")
    checkonline = [i for i in online]
    user = []
    for i in checkonline:
        if str(arg) in i:
            user.append(arg)
    if user:
        await ctx.send(f"{arg} is **online**")
    else:
        await ctx.send(f"{arg} is **offline**")

                   


# INVITE LINKS

@client.command(name='invite')
@commands.cooldown(1, 60, commands.BucketType.user)
@commands.has_any_role("Admin", "Mods")
async def _invite(ctx, *, duration : int):
    invitelink = await ctx.channel.create_invite(max_age=duration)
    await ctx.send("Invite: " + str(invitelink))





######################### RANDOM PICK ###################################



@client.command(name="randomrole")
@commands.has_any_role("Admin", "Mods")
async def _sorteocolor(ctx):
    online = []
    colors = ["cool", "skid"]
    mods = ["Admin", "Mods"]

    for member in client.get_all_members():
        if str(member.status) == "online":
            for roles in ctx.guild.roles:
                if roles.name in mods:
                    pass
                else:
                    online.append(member)
    randomuser = random.choice(online)
    randomcolors = random.choice(colors)
    randomrole = discord.utils.get(member.guild.roles, name=randomcolors)
    await member.add_roles(randomrole)
    await ctx.send(f"User: **{randomuser}**, Role: **{randomrole}**")


#############################################################################




############################## TOOLS #########################################


# MD5

@client.command(name="md5hash")
async def _md5hash(ctx, *, arg):
    hash_object = hashlib.md5(arg.encode())
    md5 = hash_object.hexdigest()
    file = discord.File("img/root.png", filename="root.png")
    embed = discord.Embed(colour = discord.Colour.blue())
    embed.set_thumbnail(url='attachment://root.png')
    embed.set_author(name="IP ADDRESS") 
    embed.add_field(name='Text', value=arg, inline=False)
    embed.add_field(name='MD5', value=md5, inline=False)
    await ctx.send(file=file, embed=embed)    



# GET IP ADDRESS

@client.command(name="getip")
async def _getipaddress(ctx, *, arg):
    try:
        ip = socket.gethostbyname(arg)
        file = discord.File("img/root.png", filename="root.png")
        embed = discord.Embed(colour = discord.Colour.blue())
        embed.set_thumbnail(url='attachment://root.png')
        embed.set_author(name="IP ADDRESS") 
        embed.add_field(name='Site', value=arg, inline=False)
        embed.add_field(name='IP', value=ip, inline=False)
        await ctx.send(file=file, embed=embed)
    except socket.error:
        file = discord.File("img/root.png", filename="root.png")
        embed = discord.Embed(colour = discord.Colour.blue())
        embed.set_thumbnail(url='attachment://root.png')
        embed.set_author(name="IP ADDRESS") 
        embed.add_field(name='Site', value=arg, inline=False)
        embed.add_field(name='IP', value="NOT FOUND", inline=False)
        await ctx.send(file=file, embed=embed)


# Site recon

@client.command(name="recon")
async def _ideas(ctx, *, site):
    conn = http.client.HTTPConnection(site)
    conn.connect()
    conn.request('OPTIONS', '/')
    response = conn.getresponse()
    heading = response.getheader('allow')
    check = response.getheader('allow')
    w = whois.whois(site)
    w = dict(w)
    domain_name = "Domain_Name: {} ".format(w["domain_name"]) + "\n"
    registrar = "Registrar: {} ".format(w["registrar"]) + "\n"
    whois_server =  "Whois_Server: {} ".format(w["whois_server"]) + "\n"
    name_servers = "Name_Server: {} ".format(w["name_servers"])
    whois_resp = str(domain_name) + str(registrar) + str(whois_server) + str(name_servers)
    print (w)
    try:
        info = dns.resolver.query(site, 'MX')
        for rdata in info:
            exchange = rdata.exchange
            preference = rdata.preference
            time.sleep(0.5)
        
        ip = socket.gethostbyname(site)
        if "https" not in site:
            site = "https://" + site
        elif "http" not in site:
            site = "http://" + site
        resp = requests.head(site)
        ua = UserAgent(verify_ssl=False)
        header = {'User-Agent':str(ua.chrome)}		
        response = requests.get(site, headers=header).status_code
    except:
        pass
    embed = discord.Embed( 
        title = 'reconnaissance',
        colour = discord.Colour.blue()
    )
    file = discord.File("img/recon.png", filename="recon.png")
    embed.set_footer(text='gotr00t?')
    embed.set_thumbnail(url='attachment://recon.png')
    embed.add_field(name='Target', value=site, inline=False)
    embed.add_field(name='Code', value=response, inline=False)
    embed.add_field(name='IP', value=ip, inline=False)
    embed.add_field(name='DNSLOOKUP', value=exchange, inline=False)
    embed.add_field(name='Headers', value=resp.headers, inline=False)
    embed.add_field(name='OPTIONS', value=heading, inline=False)
    embed.add_field(name='WHOIS', value=whois_resp, inline=False)
    await ctx.send(file=file, embed=embed)  


##################################################################################


# STATUS DIS

@client.command(name="status")
async def _statusdis(ctx):
    chans = []
    for guild in client.guilds:
        for channel in guild.text_channels:
            chans.append(channel)
    for i in chans:
        channels = i
    txtchans = len(guild.text_channels)
    voicechans = len(guild.voice_channels)
    users = client.get_guild(495986950478757891)
    online = 0
    idle = 0
    for member in client.get_all_members():
        if str(member.status) != "offline":
             online +=1
        if str(member.status) == "idle":
            idle +=1
    totalusers = online
    idleusers = idle 

    file = discord.File("img/root.png", filename="root.png")
    embed = discord.Embed(colour = discord.Colour.blue())
    embed.set_thumbnail(url='attachment://root.png')
    embed.set_author(name="STATUS DISCORD") 
    embed.add_field(name='Members', value=users.member_count, inline=False)
    embed.add_field(name='Online', value=totalusers, inline=False)
    embed.add_field(name='Idle', value=idleusers, inline=False)
    embed.add_field(name='Text Channels', value=txtchans, inline=False)
    embed.add_field(name='Voice Channels', value=voicechans, inline=False)
    await ctx.send(file=file, embed=embed)


# HELP

@client.command(name="help")
async def _help(ctx):
    embed = discord.Embed(
        title = 'gotr00tBot', 
        description='HELP MENU', 
        colour = discord.Colour.blue()
    )
    file = discord.File("img/root.png", filename="root.png")
    embed.set_footer(text='gotr00t?')
    embed.set_thumbnail(url='attachment://root.png')
    embed.add_field(name='status', value="Discord info", inline=False)
    embed.add_field(name='games', value="Games", inline=False)
    embed.add_field(name='google', value="google search", inline=False)
    embed.add_field(name='onlinecheck', value="onlinecheck user", inline=False)
    embed.add_field(name='md5hash', value="md5hash text", inline=False)
    embed.add_field(name='slowmode', value="slowmode seconds", inline=False)
    embed.add_field(name='getip', value="getip site.com", inline=False)
    embed.add_field(name='kick', value="kick user message", inline=False)
    embed.add_field(name='ban', value="ban user", inline=False)
    embed.add_field(name='tban', value="tban user message duration", inline=False)
    embed.add_field(name='unban', value="unban user", inline=False)
    embed.add_field(name='mute', value="mute user", inline=False)
    embed.add_field(name='invite', value="invite duration", inline=False)

    await ctx.send(file=file, embed=embed)


# Juegos

@client.command(name="games")
async def _juegos(ctx):
    embed = discord.Embed(
        title = 'gotr00tBot', 
        description='Games', 
        colour = discord.Colour.blue()
    )
    embed.set_footer(text='Discord games to play')
    embed.set_thumbnail(url='https://mk0vojovoweumgjb625j.kinstacdn.com/wp-content/uploads/2019/06/25.6.19_header.jpg')
    embed.add_field(name='$dice', value="roll the dice until you hit 7 7 7 ", inline=False)
    embed.add_field(name='$darts', value="throw the darts", inline=False)
    await ctx.send(embed=embed)   


# dados

@client.command(name="dice")
@commands.cooldown(1, 10, commands.BucketType.user)
async def _dados(ctx):
     num1 = random.randint(0,9)
     num2 = random.randint(0,9)
     num3 = random.randint(0,9)
     roller = str(num1) + " " + str(num2) + " " + str(num3)
     if roller == "7 7 7":
         await ctx.send(file=discord.File("img\\winner.jpg"))
     await ctx.send(file=discord.File("img\\dice.jpg"))
     await ctx.send(roller)

# darts

@client.command(name="darts")
async def _darts(ctx):
    throw = ["missed", "missed", "missed","missed", "missed", "missed","missed", "missed", "missed", "BULLSEYE!"]
    play = random.choice(throw)
    if play == "BULLSEYE!":
        await ctx.send("BULLSEYE!!")
    else:
        await ctx.send("MISSED!")


# Google

@client.command(name='google')
@commands.cooldown(1, 5, commands.BucketType.user)
async def _google(ctx, *, arg):
    numpage = 3
    ua = UserAgent()
    header = {'User-Agent':str(ua.chrome)}
    for url in search(arg, stop=numpage, user_agent=str(header)):
        display = url
    await ctx.send(display)

# Hablar

@client.command(name="say")
async def test(ctx, *, arg):
    await ctx.send(arg)


# Announcements

@client.command(name="announcements")
async def _ideas(ctx, *, arg):
    name = ctx.author.name
    embed = discord.Embed(
        description = arg,
        colour = discord.Colour.blue()
    )
    embed.set_footer(text=name)
    channel =  client.get_channel(536622190414528514)
    msg = await channel.send(embed=embed)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")
 


# TRANSLATOR

@client.command(name="translate")
async def _trans(ctx, arg1, arg2, *, arg3):
    translator = Translator(from_lang=arg1,to_lang=arg2)
    translation = translator.translate(arg3)
    await ctx.send(translation)


# TICKET 

@client.command(name="ticket")
async def _tickets(ctx, cat : str, *, arg):
    guild = ctx.guild
    member = ctx.author
    admin_role = discord.utils.get(guild.roles, name="Admin")
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        admin_role: discord.PermissionOverwrite(read_messages=True, send_messages=True)
    }
    name = ctx.author.name
    mention = ctx.message.author.mention
    time = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    timeanduser = name + " " + "•" + " " + time
    tckmsg = "Dear **{}**, \n\nThanks for reaching out to us, we'll do our best to respond to your question as soon as possible. You can leave any extra information in this channel if needed.".format(mention)
    num = random.randint(0,1000000000000000000)
    ticket = "ticket-" + str(num)
    guilds = ctx.message.guild
    nameofcat = cat
    category = discord.utils.get(ctx.guild.categories, name=nameofcat)
    await guilds.create_text_channel(ticket, overwrites=overwrites, category=category)
    channel = discord.utils.find(lambda c: c.name == str(ticket), guilds.text_channels)
    if channel is not None:
        embed = discord.Embed(
            title  = "Support Ticket",
            description = tckmsg,
            colour = discord.Colour.blue()
        )
        embed.set_footer(text=timeanduser)
        embed.add_field(name='**Ticket Reason**', value=arg, inline=False)
        txtchannel =  client.get_channel(channel.id)
        await txtchannel.send(embed=embed)
        msgticket = "new #{} was created by {}".format(ticket, name)
        for members in client.get_all_members():
            for role in members.roles:
                if role.name == "Admin":
                    await members.send(msgticket)




client.run(token)
