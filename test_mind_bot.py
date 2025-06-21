from mcstatus import JavaServer
import discord
from discord.ext import commands
import re
import threading
import time

intents = discord.Intents.default()
intents.message_content = True
intents.typing = True
bot = commands.Bot(command_prefix='!', intents=intents)
server = None
status = None

def DoubleFlow(): #Запуск функции для второго потока
    global status #Для редактирования функции
    while True:
        if server != None:
            try:
                status = server.status()
            except TimeoutError:
                time.sleep(30)
        time.sleep(10) #10 секунд для повторения



updateThread = threading.Thread(target=DoubleFlow, daemon=True)
updateThread.start()

#Получение данных о игроках и удаленние ненужной информации
def scaner():
    n = 0
    finalList = ''
    for n in range(n, status.players.online):
        listStr = str(status.players.sample[n]) # Получаем часть списка для редактирования
        listStr = re.sub('JavaStatusPlayer','',listStr)
        listStr = re.sub('name=','',listStr)
        listStr = re.sub(", id='(.*)'",'',listStr) + "\n" #Убираем ненужное
        finalList+= listStr #Добавляем в финальное сообщение

    return finalList

@bot.event
async def on_ready():
    print("Электронный шум") #Для проверки работоспособности

@bot.command()
async def echo(message): #Комманда !echo
    if server == None:
        await message.send('Не найденны данные для сканирования. Воспользуйтесь функцией "!writeip" чтобы записать ip адресс')
    else:
        n = 0
        finalMes = scaner() #Вызываем функцию для получения данных
        await message.send(f"Число онлайна: {status.players.online}") #Вывод количества игроков на сервер
        await message.send("```" + finalMes +"```") # Вывод в сообщении всех игроков на сервере

@bot.command()
async def writeip(message, *, text=None):
    global server
    global status
    if text!=None:
        server = JavaServer.lookup(str(text))
        try:
            status = server.status()
        except TimeoutError:
            await message.send("Данный айпи адресс не сканируется")
            return
        await message.send("Айпи успешно получени")
    else:
        await message.send("Напиши айпи перед сообщением")



bot.run('ur ')
