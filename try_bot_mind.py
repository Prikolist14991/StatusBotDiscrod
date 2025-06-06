from mcstatus import JavaServer
import discord
from discord.ext import commands
import re


intents = discord.Intents.default()
intents.message_content = True
intents.typing = True
bot = commands.Bot(command_prefix='!', intents=intents)
server = JavaServer.lookup("ur ip")
status = server.status()

def scaner():
    n = 0
    finalList = ''
    for n in range(n, status.players.online):
        if status.players.online>0 and n == 1:
            listStr +="('Player')"
        listStr = str(status.players.sample[n])
        listStr = re.sub('JavaStatusPlayer','',listStr)
        listStr = re.sub('name=','',listStr)
        listStr = re.sub(", id='(.*)'",'',listStr) + "\n"
        finalList+= listStr
        
    return finalList


@bot.event
async def on_ready():
    print(f"Электронный шум")

@bot.command()
async def echo(message):
    n = 0
    finalMes = scaner()
    message.send(f"Число онлайна: {status.players.online}")
    message.send("```" + finalMes +"```")

bot.run('ur token')
