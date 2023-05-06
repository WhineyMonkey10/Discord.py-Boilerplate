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
            print(colorama.Fore.GREEN + "Bot ready to use!")
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
                await ctx.send("Please enter the role id of the role that has permissions to use the bot")
                message = await bot.wait_for('message', check=check)
                permissionsRoleID = message.content
                
                with open("botData/roleIDs.txt", "w") as f:
                    f.write(botRoleID + "\n" + permissionsRoleID)
                    f.close()
                
                await ctx.send("Bot setup complete!")
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
                await ctx.send("Please enter the role id of the role that has permissions to use the bot")
                message = await bot.wait_for('message', check=check)
                permissionsRoleID = message.content
                
                with open("botData/roleIDs.txt", "w") as f:
                    f.write(botRoleID + "\n" + permissionsRoleID)
                    f.close()
                
                await ctx.send("Bot setup complete!")
                

# Main commands

@bot.command()
async def ping(ctx):
    before = time.monotonic()
    message = await ctx.send("Pong!")
    await message.edit(content="Calculating ping...")
    await message.edit(content=f"Calculated ping: {round((time.monotonic() - before) * 1000)}ms")

    
    
     


bot.run(botToken)
    