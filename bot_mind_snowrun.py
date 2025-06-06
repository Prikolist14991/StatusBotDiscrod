from mcstatus import JavaServer
import discord
from discord.ext import commands
import re
import asyncio
import random

colorList = ["[1;31m","[1;32m","[1;33m","[1;34m"] #Цвета ansi для дискорда
noiseList = ["∎","▯","▰","$","*","#","☒","-","/"] #Символы для создания "шума". Можно вписывать все что угодно

#Следующий сегмент является подключением дискорд классов и получения статуса сервера
intents = discord.Intents.default()
intents.message_content = True
intents.typing = True
bot = commands.Bot(command_prefix='!', intents=intents)
server = JavaServer.lookup("ur ip") #сюда адресс сервера
status = server.status()

#minEdit - количество минут, необходимые для паузы между обновлениями списка
minEdit = 1
timer = minEdit*60

#Функция, которая изменяет часть текста на цифры и другие символы
def replace(input_str, num_chars_to_replace):
    if not input_str: #проверка строки
        return input_str
    str_list = list(input_str) #Перевод str в list для редактирования текста
    indices_to_replace = random.sample(range(len(str_list)), num_chars_to_replace)#выбор некоторых символов для их замены
    for index in indices_to_replace:# Вместо сида или маски используется достаточно стабильный метод,
        #при помощи которого каждый четный элемент заменяется цифрой, а не четный - символом из списка
        if index % 2 == 0:
            str_list[index] = str(random.randint(0, 9)) #Случайный выбор от 0 до 9
        elif index % 2 == 1:
            str_list[index] = noiseList[random.randint(0,len(noiseList)-1)] #Случайный выбор в списке от нулевого элемента до последнего
    return ''.join(str_list) #Возвращяем текст

#Вывод текст в зависимости от количества игроков на сервере
def online():
    if status.players.online == 0:
        return "Неопределенное число разумных существ в зоне действия сканера"
    elif status.players.online <=5:
        return "Малое количество разумных существ в зоне действия сканера. Не более 5"

    elif status.players.online <=10:
        return "Среднее количество разумных существ в зоне действия сканера. В районе " + str(random.randint(4,13))
    elif status.players.online > 10:
        return "Высокое количество разумных существ в зоне действия сканера. Меньше " + str(status.players.max+1)

#Редактирует запрос из API в нормальный и читаемый str
def scaner():
    n = 0
    listStr = ""
    finalList=""
    for n in range(n, status.players.online): #Цикл от 0 до количества игроков онлайн
        if status.players.online>0 and n == 1: #Создание "фейкового" игрока. Происходит если хотя бы один игрок есть на сервере
            listStr +="('Player')" #Благодаря replace текст одинаковые строки Player становятся P16laer, Pla712@ и так далее...
        listStr = str(status.players.sample[n]) #Перевод элемента list[JavaStatusPlayer] в str
        listStr = re.sub('JavaStatusPlayer','',listStr) #Удаление ненужной информации со строки
        listStr = re.sub('name=','',listStr)
        listStr = re.sub(", id='(.*)'",'',listStr)
        finalList+= listStr #Суммируем итоговое сообщение и полученную строку
        finalList+="\n"
    return finalList

#Формирует финальное сообщение
def formerMess():
    finalList = scaner()
    finalList = replace(finalList,random.randint(status.players.online*4,status.players.online*10)) #Рандомизируем "искажения" текста в зависимости от игроков
    finalMes = online()
    finalMes = replace(finalMes,random.randint(10,20)) #Рандомизируем "искажения" вступительного текста
    return ("```ansi\n" + colorList[random.randint(0,len(colorList)-1)]
    +finalMes + "\n"
    + finalList
    +"```")

#отправитель сообщений без использования message
async def sender(channel_id: int, msg):
    channel = bot.get_channel(channel_id)
    await channel.send(msg)

#Отправка сообщений в лог и на сервер при запуске бота
@bot.event
async def on_ready():
    print(f"Электронный шум")
    asyncio.run_coroutine_threadsafe(sender(1362303025741566013, '*Звук включения тумблера*'), bot.loop)

#Бесконечное событие изменяющий текст последнего сообщения (из on_ready)
@bot.event
async def on_message(message):
    while True: #Запуск бесконечного цикла
        await asyncio.sleep(timer)#Таймер-пауза между редактированием текста
        finallyMess = formerMess() #Формируем последнее сообщение
        if message.author == bot.user: #Сравнение последних сообщений
            lastMessageId = message.id
            channel = message.channel
        if message.author == bot.user and lastMessageId:
            editMessage = await channel.fetch_message(lastMessageId)
            await editMessage.edit(content=finallyMess) #Редактирование сообщения
        else: print("Перебои связи") #В случае ошибок

#НЕ советуется писать в чат для бота так как бот проверяет последнее сообщение в канале, а не последнее свое сообщение




bot.run('ur token') #вписывай токен своего бота
