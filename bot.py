import asyncio
import discord
import os
from os.path import isfile, dirname, realpath
from mcstatus import MinecraftServer
from discord.ext import commands
from discord.ext import tasks

# Bot variables.
bot = commands.Bot(command_prefix='!')
bot.remove_command('help')
modules = ["fun", "moderation", "administration"]
offlineSent = False

# Server status query.
@tasks.loop(seconds=10.0)
async def set_status():
    global offlineSent
    try:
        server = MinecraftServer.lookup("51.91.61.56:41435")
        status = server.status()
        
        if offlineSent:
            channel = bot.get_channel(793501401832620072)
            embed=discord.Embed(title="🟢 SERVER IS BACK ONLINE", description="We're back! Come join us again.", color=0x54ce4b)
            await channel.send(embed=embed)
            offlineSent = False

        if status.players.online == status.players.max:
            pres, msg = discord.Status.idle, f"a full server! ({status.players.online}/{status.players.max})"
        else:
            pres, msg = discord.Status.online, f"{status.players.online}/{status.players.max} players."
    except ConnectionRefusedError:
        channel = bot.get_channel(793501401832620072)
        pres, msg = discord.Status.dnd, "server is offline!"

        if not offlineSent:
            embed=discord.Embed(title="🔴 SERVER IS NOW OFFLINE", description="We'll be back soon! If the server does not come back up, please @ a big brain.", color=0xff4238)
            await channel.send(embed=embed)
            offlineSent = True
        
    await bot.change_presence(status=pres,activity=discord.Activity(type=discord.ActivityType.watching, name=msg))
    print(f"> Successful query! Status updated to: {msg}")

# Status command.
@bot.command()
async def status(ctx):
    try:
        server = MinecraftServer.lookup("51.91.61.56:41435")
        status, query = server.status(), server.query()

        embed=discord.Embed(title="🟢 ONLINE", color=0x54ce4b)
        embed.add_field(name="Server Status", value="Online", inline=True)
        embed.add_field(name="Player Count", value=status.players.online, inline=True)
        embed.add_field(name="Server Ping", value=f'{status.latency}ms', inline=True)
        embed.add_field(name="Online Players", value=query.players.names, inline=False)
        embed.set_footer(text=f"Requested by {ctx.message.author}")
        await ctx.send(embed=embed)
    except ConnectionRefusedError:
        embed=discord.Embed(title="🔴 OFFLINE", description="We'll be back soon! :(", color=0xff4238)
        embed.set_footer(text=f"Requested by {ctx.message.author}.")
        await ctx.send(embed=embed)

# Dynmap command.
@bot.command()
async def dynmap(ctx):
    await ctx.send("🗺️ The dynmap can be found here: http://51.91.61.56:11435/")

# IP command.
@bot.command()
async def ip(ctx):
    await ctx.send("🖥️ Connect via `mypeeburns.serv.gs` or `51.91.61.56:41435`. Make sure you're whitelisted!")

@bot.command()
@commands.has_any_role("🧠 Big Brain")
async def load(ctx, extension):

    author = ctx.message.author
    extension = extension.lower()

    loadnotify_success = discord.Embed(
        title = f':white_check_mark: Loaded {extension}.',
        colour = discord.Colour.green()
    )

    loadnotify_success.set_footer(text=f'Requested by {author}', icon_url=ctx.author.avatar_url)

    loadnotify_failed = discord.Embed(
        title = f':skull_crossbones: Could not load {extension}.',
        description = "Error: module not found!",
        colour = discord.Colour.red()
    )

    loadnotify_failed.set_footer(text=f'Requested by {author}', icon_url=ctx.author.avatar_url)

    if extension in modules:
        bot.load_extension(f'cogs.{extension}')
        await ctx.send(embed=loadnotify_success)
    else:
        await ctx.send(embed=loadnotify_failed)
    print(f'[MODULE] {author} loaded {extension}.')

@bot.command()
@commands.has_any_role("🧠 Big Brain")
async def unload(ctx, extension):

    author = ctx.message.author
    extension = extension.lower()

    unloadnotify_success = discord.Embed(
        title = f':white_check_mark: Unloaded {extension}.',
        colour = discord.Colour.green()
    )

    unloadnotify_success.set_footer(text=f'Requested by {author}', icon_url=ctx.author.avatar_url)

    unloadnotify_failed = discord.Embed(
        title = f':skull_crossbones: Could not unload {extension}.',
        description = "Error: module not found!",
        colour = discord.Colour.red()
    )

    unloadnotify_failed.set_footer(text=f'Requested by {author}', icon_url=ctx.author.avatar_url)

    if extension in modules:
        bot.unload_extension(f'cogs.{extension}')
        await ctx.send(embed=unloadnotify_success)
    else:
        await ctx.send(embed=unloadnotify_failed)
    print(f'[MODULE] {author} unloaded {extension}.')

@bot.command()
@commands.has_any_role("🧠 Big Brain")
async def reload(ctx, extension):

    author = ctx.message.author
    extension = extension.lower()

    reloadnotify_success = discord.Embed(
        title = f':white_check_mark: Reloaded {extension}.',
        colour = discord.Colour.green()
    )

    reloadnotify_success.set_footer(text=f'Requested by {author}', icon_url=ctx.author.avatar_url)

    reloadnotify_failed = discord.Embed(
         title = f':skull_crossbones: Could not reload {extension}.',
        description = "Error: module not found!",
        colour = discord.Colour.red()
    )

    reloadnotify_failed.set_footer(text=f'Requested by {author}', icon_url=ctx.author.avatar_url)

    if extension in modules:
        bot.unload_extension(f'cogs.{extension}')
        bot.load_extension(f'cogs.{extension}')
        await ctx.send(embed=reloadnotify_success)
    else:
        await ctx.send(embed=reloadnotify_failed)
    print(f'[MODULE] {author} reloaded {extension}.')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

# On ready event.
@bot.event
async def on_ready():
    divider = "============================="
    print(f'\n{divider}\nLogged in as {bot.user}!\n{divider}\n')
    await set_status.start()

# Run bot.
bot.run(os.environ['token'])