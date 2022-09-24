from sys import argv
from xmlrpc.client import NOT_WELLFORMED_ERROR
import discord
from discord.ext import commands
import requests
import os
from dotenv import load_dotenv
import random
import multiprocessing
from datetime import datetime

BOT_NAME = "FifaBot"
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_GUILD = os.getenv("DISCORD_GUILD")

intents = discord.Intents(messages=True,message_content=True, guilds=True)
#client = discord.Client( intents= intents )
available_commands = ['help', 'serverusage', 'serverstatus', 'jugador']

# Set the bot command prefix
bot = commands.Bot(command_prefix="!", intents= intents )
bot_help_message = """
:: Bot Usage ::
`!fifa help`                   : shows help
`!fifa serverusage`   : shows system load in percentage
`!fifa serverstatus` : shows if the server is online or offline
`!fifa jugador (Player name)`   : shows player information
"""

# Executes when the bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user} succesfully logged in!')

@bot.event
async def on_ready():
    print(bot.guilds)
    guild = discord.utils.find(lambda g: g.name == DISCORD_GUILD, bot.guilds)
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@bot.event
async def on_message(message):
    print(format(message.content))
    # Evitar bucle
    if message.author == bot.user:
        return
    
    channel = message.channel

    #await channel.send('Faltan ' + str(datetime.now() - datetime.strptime("2022-09-30", '%Y-%m-%d')) + ' para el Fifa23')
    #if 'fifa' in message.content.lower():
     #   await message.channel.send('Happy Birthday! 🎈🎉')
    if message.content == '!fifa':
        await channel.send('Faltan ' + str(datetime.now() - datetime.strptime("2022-09-30", '%Y-%m-%d')) + ' para el Fifa23')
        await message.channel.send(bot_help_message)
    if 'jugador' in message.content.lower():
        nombre_jugador = message.content[13:].strip()
        print(f'{message.author} busca a {nombre_jugador}')
        await channel.send(f'{message.author} busca a {nombre_jugador}')
    await bot.process_commands(message)
        
@bot.command()
async def fifa(ctx, arg):
    if arg == 'help':
        await ctx.send(bot_help_message)
    if arg == 'jugador':
        print(format(arg), format(ctx))
        await ctx.send(f' Envio - {arg}')

bot.run(DISCORD_TOKEN)


#https://blog.ruanbekker.com/blog/2022/05/05/create-a-discord-bot-in-python/