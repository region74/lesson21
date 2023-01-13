import telebot
import time
import pprint
import os

TOKEN = ''
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['restart'])
def restart_server(message):
    # выполниь команду операционки через питон
    os.system('shutdown -r -t 0')


bot.infinity_polling()
