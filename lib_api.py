import telebot
import time
import pprint
import os

TOKEN = '5914159692:AAHEr0XfUxEeryUovHjmHO-x3WDuy13a-r4'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Че кого?")


@bot.message_handler(commands=['restart'])
def restart_server(message):
    # выполниь команду операционки через питон
    os.system('notepad')


# команда администратора если потом надо куда то дальше идти
@bot.message_handler(commands=['admin'], func=lambda message: message.from_user.username == 'ignatov23')
def admin(message):
    info = os.name
    bot.reply_to(message, info)


# это если не надо куда-то дальше идти
@bot.message_handler(commands=['admin2'])
def admin2(message):
    if message.from_user.username == 'ignatov23':
        info = os.name
        bot.reply_to(message, info)
    else:
        bot.reply_to(message, 'Ацтань')


@bot.message_handler(commands=['timer'])
def timer(message):
    for i in range(5):
        time.sleep(1)
        bot.send_message(message.chat.id, i + 1)


@bot.message_handler(commands=['say'])
def say(message):
    print(message)
    # получить то что после команды
    text = ' '.join(message.text.split(' ')[1:])
    bot.reply_to(message, text)


@bot.message_handler(commands=['file'])
def get_file(message):
    # передать файл с диска
    with open('text.txt', 'r', encoding='utf-8') as data:
        bot.send_document(message.chat.id, data)


@bot.message_handler(commands=['pic'])
def get_file(message):
    # передать файл с диска
    with open('pict.jpg', 'rb') as data:
        bot.send_photo(message.chat.id, data)


@bot.message_handler(content_types=['text'])
def reverse_text(message):
    if 'плохой' in message.text.lower():
        bot.reply_to(message, 'асуждаю')
        return
    # text = message.text[::-1]
    text = message.text

    bot.reply_to(message, text)


@bot.message_handler(content_types=['sticker'])
def send_sticker(message):
    FILE_ID = 'CAACAgIAAxkBAANMY8ESxMT8XZ-6lhBZHW2OUPaejwkAAkYDAAK1cdoG8qJR41YTMIwtBA'
    bot.send_sticker(message.chat.id, FILE_ID)


bot.infinity_polling()
