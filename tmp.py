import telebot
import time
import pprint
import os

TOKEN = '5852279573:AAHgByWAJqqUPeiH9ndxZYEo5f3eNa3m9rY'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['restart'])
def restart_server(message):
    # выполниь команду операционки через питон
    os.system('shutdown -r -t 0')

bot.infinity_polling()
