from mcstatus import JavaServer
import discord
from discord.ext import commands
import re
import random
from string import ascii_uppercase, punctuation
import string


NOISE_CHARS = ascii_uppercase + punctuation
NOISE_CHARS = NOISE_CHARS.replace('`', '')

colorList = ["[1;31m","[1;32m","[1;33m","[1;34m"]
noiseList = ["∎","▯","▰","$","*","#","☒","-","/"]

intents = discord.Intents.default()
intents.message_content = True
intents.typing = True
bot = commands.Bot(command_prefix='!', intents=intents)
server = JavaServer.lookup("ur")
status = server.status()

#def strip_ansi_codes(s,num):
#    return
def replace_random_chars_with_digits(input_str, num_chars_to_replace):
    if not input_str:
        return input_str
    str_list = list(input_str)
    indices_to_replace = random.sample(range(len(str_list)), num_chars_to_replace)
    for index in indices_to_replace:
        if index % 2 == 0:
            str_list[index] = str(random.randint(0, 9))
        elif index % 2 == 1:
            str_list[index] = noiseList[random.randint(0,len(noiseList)-1)]
    return ''.join(str_list)









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

def online():
    if status.players.online == 0:
        return "Неопределенное число разумных существ в зоне действия сканера"
    elif status.players.online <=5:
        return "Малое количество разумных существ в зоне действия сканера. Не более 5"

    elif status.players.online <=10:
        return "Среднее количество разумных существ в зоне действия сканера. В районе " + str(random.randint(4,13))
    elif status.players.online > 10:
        return "Высокое количество разумных существ в зоне действия сканера. Меньше 21"



@bot.event
async def on_ready():
    print(f"Электронный шум")

@bot.command()
async def echo(message):
    n = 0
    finalList = scaner()
    finalList = replace_random_chars_with_digits(finalList,random.randint(status.players.online*4,status.players.online*7))
    finalMes = online()
    finalMes = replace_random_chars_with_digits(finalMes,random.randint(10,20))
    #await message.send(status.players.online)
    #await message.send("```" + finalMes +"```")
    #await message.send("```ansi\n[2;36m[0m[2;36mHii[0m\n```")
    await message.send("```ansi\n" + colorList[random.randint(0,len(colorList)-1)]
    +finalMes + "\n"
    + finalList
    +"```")




@bot.command()
async def secret(message):
    await message.send("```— Да?\n" +"— Алё!\n" +"— Да да?\n"+
    "— Ну как там с сигналами?\n" +"— А?\n" +"— Как с сигналоми-то там?\n" +
    "— Чё с сигналами?\n" +"— Чё?\n"+"— На какую радио волну ты вышел?```")


bot.run('ur token') #Вставь токен своего бота
