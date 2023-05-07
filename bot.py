# Created by @WhineyMonkey10
# WhineyMonkey10 on GitHub, WhineyMonkey10#9162 on Discord

# Imports

## Discord Imports

import discord
from discord.ext import commands

## System Imports

import os

## Connfiguration Imports

from dotenv import load_dotenv

## Other Imports

import colorama
import random
import time


### Setup Configurations

load_dotenv()

botToken = str(os.getenv("TOKEN"))
botPrefix = os.getenv("PREFIX")
botStatus = os.getenv("STATUS")
permissionsRoleID = os.getenv("PERMISSIONS_ROLE_ID")

# Check and or create the botData folder
if os.path.exists("botData"):
    pass
else:
    os.mkdir("botData")


## Main Code (For now, no comments or clean code will be added beyond this point)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
intents.guilds = True
intents.guild_messages = True
intents.guild_reactions = True
intents.guild_typing = True
intents.dm_messages = True
intents.dm_reactions = True
intents.dm_typing = True
intents.bans = True
intents.emojis = True
intents.integrations = True
intents.invites = True
intents.voice_states = True
intents.webhooks = True

bot = commands.Bot(command_prefix=botPrefix, intents=intents)


def checkIfBotIsConfigured():
    if os.path.exists("botData/setup.txt"):
        with open("botData/setup.txt", "r") as f:
            if f.read() == "1":
                return True
            else:
                return False
            
def setEnvVariable(variableName, value):
    with open(".env", "a") as f:
        f.write("\n" + variableName + "=" + value)
        f.close()



@bot.event
async def on_ready():
    print(colorama.Fore.GREEN + f"Logged in as {bot.user.name}#{bot.user.discriminator} ({bot.user.id})")
    await bot.change_presence(activity=discord.Game(name=botStatus))
    print(colorama.Fore.GREEN + f"Status set to {botStatus}")
    if os.path.exists("botData/setup.txt"):
        print(colorama.Fore.GREEN + "Bot already setup!")
        print(colorama.Fore.GREEN + "Confirming configuration...")
        
        with open("botData/roleIDs.txt", "r") as f:
            botRoleID = f.readline().strip()
            permissionsRoleID = f.readline().strip()
            
            print(colorama.Fore.GREEN + "Bot role id: " + botRoleID)
            print(colorama.Fore.GREEN + "Permissions role id: " + permissionsRoleID)
            print(colorama.Fore.GREEN + "The bot is ready to use!")
    else:
        print(colorama.Fore.RED + "Bot not setup! Please run the command    {}{}{}setupBot{}    to setup the bot!{}{}".format(colorama.Fore.GREEN, colorama.Style.BRIGHT, botPrefix, colorama.Fore.RED, colorama.Style.RESET_ALL, colorama.Fore.RESET))
            
    
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

@bot.command()
async def setupBot(ctx):
    await ctx.send("Setting up bot...")
    
    if os.path.exists("botData/setup.txt"):
        with open("botData/setup.txt", "r") as f:
            if f.read() == "1":
                await ctx.send("Bot already setup!")
    else:        
        with open("botData/setup.txt", "w") as f:
            pass
            f.close()
        
        with open("botData/setup.txt", "r") as f:
            if f.read() == "1":
                await ctx.send("Bot already setup!")
            else:
                f.close()
                await ctx.send("Bot not setup! Setting up...")
                with open("botData/setup.txt", "w") as f:
                    f.write("1")
                    f.close()
                await ctx.send("Confirming configuration...")
                await ctx.send("Bot prefix: " + botPrefix)
                await ctx.send("Bot status: " + botStatus)
                
                await ctx.send("Please enter the role id of the role that will be used for the bot")
                def check(message):
                    return message.author == ctx.author and message.channel == ctx.channel
                message = await bot.wait_for('message', check=check)
                botRoleID = message.content
                await ctx.send("Please enter the name of the role that has permission to use the bot (case sensitive)")
                message = await bot.wait_for('message', check=check)
                permissionsRoleID = message.content
                
                with open("botData/roleIDs.txt", "w") as f:
                    f.write(botRoleID + "\n" + permissionsRoleID)
                    f.close()
                
                with open(".env", "a") as f:
                    f.write("\nPERMISSIONS_ROLE_ID=" + permissionsRoleID)
                    f.close()
                
                await ctx.send("Creating config, log and storage files...")
                
                os.mkdir("botData/punishments")
                os.mkdir("botData/punishments/logs")
                
                with open("botData/punishments/warns.txt", "x") as f:
                    pass
                    f.close()
                with open("botData/punishments/logs/mutes.txt", "x") as f:
                    pass
                    f.close()
                with open("botData/punishments/logs/kicks.txt", "x") as f:
                    pass
                    f.close()
                with open("botData/punishments/logs/bans.txt", "x") as f:
                    pass
                    f.close()
                
                await ctx.send("Bot setup complete!")
                

# Main commands

@bot.command()
async def ping(ctx):
    if checkIfBotIsConfigured() == False:
        embed = discord.Embed(title="Bot not setup!", description="Please run the command `{}setupBot` to setup the bot!".format(botPrefix), color=discord.Color.blue())
        await ctx.send(embed=embed)
        return
    else:
        before = time.monotonic()
        message = await ctx.send("Pong!")
        await message.edit(content="Calculating ping...")
        embed = discord.Embed(title="Pong!", description=f"Calculated ping: {round((time.monotonic() - before) * 1000)}ms", color=discord.Color.blue())
        await message.edit(embed=embed)

@bot.command()
@commands.has_role(os.getenv("PERMISSIONS_ROLE_ID"))
async def warn(ctx, member: discord.Member, *, reason=None):
    if checkIfBotIsConfigured() == False:
        embed = discord.Embed(title="Bot not setup!", description="Please run the command `{}setupBot` to setup the bot!".format(botPrefix), color=discord.Color.blue())
        await ctx.send(embed=embed)
        return
    else:
        if reason == None:
            embed = discord.Embed(title="Please specify a reason!", color=discord.Color.blue())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Warning issued!", description="{} has been warned for: {}".format(member.mention, reason), color=discord.Color.blue())
            await ctx.send(embed=embed)
            if os.path.exists("botData/punishments/warns.txt"):
                with open("botData/punishments/warns.txt", "a") as f:
                    f.write(str(member.id) + ":" + reason + "\n")
                await member.send("You have been warned for " + reason)
                embed = discord.Embed(title="Warning issued!", description="If they have DMs enabled, they will be notified!", color=discord.Color.blue())
                await ctx.send(embed=embed)

@bot.command()
@commands.has_role(os.getenv("PERMISSIONS_ROLE_ID"))
async def getWarns(ctx, member: discord.Member):
    if checkIfBotIsConfigured() == False:
        embed = discord.Embed(title="Bot not setup!", description="Please run the command `{}setupBot` to setup the bot!".format(botPrefix), color=discord.Color.blue())
        await ctx.send(embed=embed)
        return
    else:
        with open("botData/punishments/warns.txt", "r") as f:
            warns = f.readlines()
            f.close()
        embed = discord.Embed(title="Getting warns...", color=discord.Color.blue())
        message = await ctx.send(embed=embed)
        warnList = []
        for warn in warns:
            if str(member.id) in warn:
                warn = warn.replace(str(member.id) + ":", "Reason: ")
                warnList.append(warn)
        if len(warnList) == 0:
            embed = discord.Embed(title="No warns found for this user!", color=discord.Color.blue())
            await message.edit(embed=embed)
        else:
            embed = discord.Embed(title="Warns found!", description="This user has {} warn(s)!".format(str(len(warnList))), color=discord.Color.blue())
            await message.edit(embed=embed)
            
            # Format the warnList to be in a nice format
            formattedWarnList = ""
            for warn in warnList:
                formattedWarnList = formattedWarnList + warn
            embed = discord.Embed(title="Warns", description=formattedWarnList, color=discord.Color.blue())
            await ctx.send(embed=embed)
            
@bot.command()
@commands.has_role(os.getenv("PERMISSIONS_ROLE_ID"))
async def kick(ctx, member: discord.Member, *, reason=None):
    if checkIfBotIsConfigured == False:
        embed = discord.Embed(title="Bot not setup!", description="Please run the command `{}setupBot` to setup the bot!".format(botPrefix), color=discord.Color.blue())
        await ctx.send(embed=embed)
        return
    else:
        if reason == None:
            embed = discord.Embed(title="Please specify a reason!", color=discord.Color.blue())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Kicked!", description="{} has been kicked for: {}".format(member.mention, reason), color=discord.Color.blue())
            await ctx.send(embed=embed)
            await member.kick(reason=reason)
            if os.path.exists("botData/punishments/logs/kicks.txt"):
                with open("botData/punishments/logs/kicks.txt", "a") as f:
                    f.write(str(member.id) + ":" + reason + "\n")
                    f.close()
@bot.command()
@commands.has_role(os.getenv("PERMISSIONS_ROLE_ID"))
async def mute(ctx, member: discord.Member, *, reason=None):
    if checkIfBotIsConfigured == False:
        embed = discord.Embed(title="Bot not setup!", description="Please run the command `{}setupBot` to setup the bot!".format(botPrefix), color=discord.Color.blue())
        await ctx.send(embed=embed)
        return
    else:
        muted_role_name = os.getenv("MUTED_ROLE_ID")
        if muted_role_name is None:
            embed = discord.Embed(title="Muted role not found!", description="Would you like to create the muted role? (y/n)", color=discord.Color.blue())
            await ctx.send(embed=embed)
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel
            msg = await bot.wait_for('message', check=check)
            if msg.content == "y":
                role = await ctx.guild.create_role(name="Muted", reason="Muted role created by the bot!")
                await role.edit(permissions=discord.Permissions(send_messages=False, read_messages=True))
                setEnvVariable("MUTED_ROLE_ID", role.name)
                embed = discord.Embed(title="Muted role created!", description="The muted role has been created!", color=discord.Color.blue())
                await ctx.send(embed=embed)
                muted_role_name = role.name
            else:
                embed = discord.Embed(title="Muted role not created!", description="The muted role has not been created!", color=discord.Color.blue())
                await ctx.send(embed=embed)
                return
        role = discord.utils.get(ctx.guild.roles, name=muted_role_name)
        if role is None:
            embed = discord.Embed(title="Muted role not found!", description="The muted role with name {} does not exist on this server. Please create the role or update the MUTED_ROLE_ID environment variable.".format(muted_role_name), color=discord.Color.blue())
            await ctx.send(embed=embed)
            return
        if role in member.roles:
            embed = discord.Embed(title="User already muted!", description="This user is already muted!", color=discord.Color.blue())
            await ctx.send(embed=embed)
            return
        else:
            if reason == None:
                embed = discord.Embed(title="Please specify a reason!", color=discord.Color.blue())
                await ctx.send(embed=embed)
                return
            else:
                await member.add_roles(role)
                embed = discord.Embed(title="Muted!", description="{} has been muted for: {}".format(member.mention, reason), color=discord.Color.blue())
                with open("botData/punishments/logs/mutes.txt", "a") as f:
                    f.write(str(member.id) + ":" + reason + "MUTED" + "\n")
                    f.close()
                await ctx.send(embed=embed)

@bot.command()
@commands.has_role(os.getenv("PERMISSIONS_ROLE_ID"))
async def unmute(ctx, member: discord.Member):
    if checkIfBotIsConfigured == False:
        embed = discord.Embed(title="Bot not setup!", description="Please run the command `{}setupBot` to setup the bot!".format(botPrefix), color=discord.Color.blue())
        await ctx.send(embed=embed)
        return
    else:
        muted_role_name = os.getenv("MUTED_ROLE_ID")
        if muted_role_name is None:
            embed = discord.Embed(title="Muted role not found!", description="Please run the command `{}mute` to create the muted role!".format(botPrefix), color=discord.Color.blue())
            await ctx.send(embed=embed)
        else:
            role = discord.utils.get(ctx.guild.roles, name=muted_role_name)
            if role not in member.roles:
                embed = discord.Embed(title="User not muted!", description="This user is not muted!", color=discord.Color.blue())
                await ctx.send(embed=embed)
                return
            else:
                await member.remove_roles(role)
                embed = discord.Embed(title="Unmuted!", description="{} has been unmuted!".format(member.mention), color=discord.Color.blue())
                with open("botData/punishments/logs/mutes.txt", "a") as f:
                    f.write(str(member.id) + ":" + "UNMUTED" + "\n")
                    f.close()
                await ctx.send(embed=embed)

@bot.command()
@commands.has_role(os.getenv("PERMISSIONS_ROLE_ID"))
async def ban(ctx, member: discord.Member, *, reason=None):
    if checkIfBotIsConfigured == False:
        embed = discord.Embed(title="Bot not setup!", description="Please run the command `{}setupBot` to setup the bot!".format(botPrefix), color=discord.Color.blue())
        await ctx.send(embed=embed)
        return
    else:
        if reason == None:
            embed = discord.Embed(title="Please specify a reason!", color=discord.Color.blue())
            await ctx.send(embed=embed)
            return
        else:
            await member.ban(reason=reason)
            embed = discord.Embed(title="Banned!", description="{} has been banned for: {}".format(member.mention, reason), color=discord.Color.blue())
            with open("botData/punishments/logs/bans.txt", "a") as f:
                f.write(str(member.id) + ":" + reason + "\n")
                f.close()
            await ctx.send(embed=embed)
    


@warn.error
async def warn_error(ctx, error):
    embed = discord.Embed(title="Permission error or command error!", color=discord.Color.blue())
    await ctx.send(embed=embed)

@getWarns.error
async def getwarns_error(ctx, error):
    embed = discord.Embed(title="Permission error or command error!", color=discord.Color.blue())
    await ctx.send(embed=embed)

@kick.error
async def kick_error(ctx, error):
    embed = discord.Embed(title="Permission error or command error!", color=discord.Color.blue())
    await ctx.send(embed=embed)

@mute.error
async def mute_error(ctx, error):
    embed = discord.Embed(title="Permission error or command error!", color=discord.Color.blue())
    await ctx.send(embed=embed)

@unmute.error
async def unmute_error(ctx, error):
    embed = discord.Embed(title="Permission error or command error!", color=discord.Color.blue())
    await ctx.send(embex=embed)

@ban.error
async def ban(ctx, error):
    embed = discord.Embed(title="Permission error or command error!", color=discord.Color.blue())
    await ctx.send(embex=embed)
    
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title="Invalid command!", description="The command you entered does not exist!", color=discord.Color.blue())
        await ctx.send(embed=embed)

    
bot.run(botToken)
    