import re
import datetime
import telebot
import random
import math
import sqlite3
from telebot import types

# Создаем бота
TOKEN = '******************'
bot = telebot.TeleBot(TOKEN)
balans = 3388.50  # текущий баланс, пока нет API сбера

reg = '^[-+]?[0-9]*[.]?[0-9]+(?:[eE][-+]?[0-9]+)?$'  # регулярка для проверки ввода

conn = sqlite3.connect('**************', check_same_thread=False)  # соединяем с бд
cursor = conn.cursor()


def db_balance_val(money: int):  # функция добавления записи баланса
    cursor.execute('INSERT INTO balance (money) VALUES (?)', [money])
    conn.commit()


def db_prihod_val(money: int):  # функция добавления записи прихода
    cursor.execute('INSERT INTO prihod (number) VALUES (?)', [money])
    conn.commit()


def db_rashod_val(money: int):  # функция добавления записи расхода
    cursor.execute('INSERT INTO rashod (number) VALUES (?)', [money])
    conn.commit()


def db_ras_val(money: int, date: datetime):  # функция добавления записи расхода с датой
    cursor.execute('INSERT INTO rashod_date (number, date) VALUES (?,?)', [money, date])
    conn.commit()


def db_pri_val(money: int, date: datetime):  # функция добавления записи прихода с датой
    cursor.execute('INSERT INTO prihod_date (number, date) VALUES (?,?)', [money, date])
    conn.commit()


def db_ras_get():  # функция получения массива расходов из БД с датой
    cursor.execute('SELECT number,date from rashod_date')
    rows = cursor.fetchall()
    l = []
    for row in rows:
        part1 = str(row[0])
        part2 = str(row[1])
        part2 = part2[:-7]
        part3 = part1 + ' руб.   ' + part2
        l.append(part3)
    conn.commit()
    str_a = ' \n'.join(map(str, l)) + '\n'
    return str_a


def db_pri_get():  # функция получения массива приходов из БД с датой
    cursor.execute('SELECT number,date from prihod_date')
    rows = cursor.fetchall()
    l = []
    for row in rows:
        part1 = str(row[0])
        part2 = str(row[1])
        part2 = part2[:-7]
        part3 = part1 + ' руб.   ' + part2
        l.append(part3)
    conn.commit()
    str_a = ' \n'.join(map(str, l)) + '\n'
    return str_a


def db_balance_get():  # функция извлечения последнего баланса из БД
    global balans
    a = cursor.execute('SELECT money from balance where + id= (select max(id) from balance)').fetchone()
    conn.commit()
    balans = float(a[0])

    return


def db_rashod_get():  # функция получения массива расходов из БД
    cursor.execute('SELECT number from rashod')
    rows = cursor.fetchall()
    l = []
    for row in rows:
        for x in row:
            l.append(x)
    conn.commit()
    str_a = ' руб.\n'.join(map(str, l)) + ' руб.'
    return str_a


def db_prihod_get():  # функция получения массива поступлений из БД
    cursor.execute('SELECT number from prihod')
    rows = cursor.fetchall()
    l = []
    for row in rows:
        for x in row:
            l.append(x)
    conn.commit()
    str_a = ' руб.\n'.join(map(str, l)) + ' руб.'
    return str_a


# Команда start
@bot.message_handler(commands=["start"])
def start(m, res=False):
    # Добавление кнопок
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Поступление 💰✅")
    item2 = types.KeyboardButton("Расходы 💸❌")
    item3 = types.KeyboardButton("Текущий баланс 👀")
    item4 = types.KeyboardButton("Выписка расходов 📝")
    item5 = types.KeyboardButton("Выписка поступлений 📝")
    item6 = types.KeyboardButton("Даты расходов")
    item7 = types.KeyboardButton("Даты поступлений")
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)
    markup.add(item4)
    markup.add(item5)
    markup.add(item6)
    markup.add(item7)
    bot.send_message(m.chat.id, 'Выбери действие: ', reply_markup=markup)


@bot.message_handler(content_types=["text"])
def handler_text(message):
    if message.text.strip() == 'Поступление 💰✅':
        sent = bot.send_message(message.chat.id, 'Введи сумму:')
        bot.register_next_step_handler(sent, inpay)
    elif message.text.strip() == 'Расходы 💸❌':
        sent = bot.send_message(message.chat.id, 'Введи сумму:')
        bot.register_next_step_handler(sent, outpay)
    elif message.text.strip() == 'Текущий баланс 👀':
        db_balance_get()  # подтягиваем баланс из бд
        bot.send_message(message.chat.id, f'{balans:.2f} рублей.')
        # db_balance_val(money=balans)
    elif message.text.strip() == 'Выписка расходов 📝':
        bot.send_message(message.chat.id, db_rashod_get())
    elif message.text.strip() == 'Выписка поступлений 📝':
        bot.send_message(message.chat.id, db_prihod_get())
    elif message.text.strip() == 'Даты расходов':
        bot.send_message(message.chat.id, db_ras_get())
        # sent = bot.send_message(message.chat.id, 'Введи сумму:')
        # bot.register_next_step_handler(sent, outpay2)
    elif message.text.strip() == 'Даты поступлений':
        bot.send_message(message.chat.id, db_pri_get())
    else:
        bot.send_message(message.chat.id, 'Некорректный запрос.')


def inpay(message):  # расчет приходов
    global balans
    text = message.text
    if text == 'Расходы 💸❌':
        bot.send_message(message.chat.id, 'Операция отменена. Введите сумму расходов:')
        bot.register_next_step_handler(message, outpay)
        return
    elif text == 'Текущий баланс 👀':
        bot.send_message(message.chat.id, f'{balans:.2f} рублей.')
        # db_balance_val(money=balans)
        return
    elif text == 'Выписка расходов 📝':
        bot.send_message(message.chat.id, db_rashod_get())
        return
    elif text == 'Выписка поступлений 📝':
        bot.send_message(message.chat.id, db_prihod_get())
        return
    elif text == 'Даты расходов':
        bot.send_message(message.chat.id, db_ras_get())
        return
    elif text == 'Даты поступлений':
        bot.send_message(message.chat.id, db_pri_get())
        return
    # if not text[0].isdigit() and text[1].isdigit():
    if re.match(reg, text) is None:
        msg = bot.send_message(message.chat.id,
                               '❗️Сумма должна быть целым или дробным числом через точку, повторите ввод: ❗️')
        bot.register_next_step_handler(msg, inpay)  # askSource
        return
    a = float(message.text)
    d = datetime.datetime.now()
    db_pri_val(money=a, date=d)  # запись прихода с датой в бд
    db_prihod_val(money=a)  # запись прихода в бд
    if a > 100000000:
        bot.send_message(message.chat.id, 'Мне кажется ты преувеличиваешь🤔\nПовтори ввод:')
        # bot.send_message(message.caht.id,'Повтори ввод:')
        bot.register_next_step_handler(message, inpay)
        return
    b = balans
    c = a + b
    balans = c
    bot.send_message(message.chat.id, 'На карту поступило: {k} рублей.'.format(k=message.text))
    bot.send_message(message.chat.id, f'Текущий баланс: {c:.2f} рублей.')
    db_balance_val(money=balans)


def outpay2(message):  # пробная для расхода с датой
    text = message.text
    a = float(message.text)
    b = datetime.datetime.now()
    db_ras_val(money=a, date=b)


def outpay(message):  # расчет расходов
    global balans
    text = message.text
    if text == 'Поступление 💰✅':
        bot.send_message(message.chat.id, 'Операция отменена. Введите сумму поступления:')
        bot.register_next_step_handler(message, inpay)
        return
    elif text == 'Текущий баланс 👀':
        bot.send_message(message.chat.id, f'{balans:.2f} рублей.')
        # db_balance_val(money=balans)
        return
    elif text == 'Выписка расходов 📝':
        bot.send_message(message.chat.id, db_rashod_get())
        return
    elif text == 'Выписка поступлений 📝':
        bot.send_message(message.chat.id, db_prihod_get())
        return
    elif text == 'Даты расходов':
        bot.send_message(message.chat.id, db_ras_get())
        return
    elif text == 'Даты поступлений':
        bot.send_message(message.chat.id, db_pri_get())
        return
    # if not text.isdigit(): #проверка что это цифры
    if re.match(reg, text) is None:
        msg = bot.send_message(message.chat.id,
                               '❗️Сумма должна быть целым или дробным числом через точку, повторите ввод: ❗️')
        bot.register_next_step_handler(msg, outpay)  # askSource
        return
    a = float(message.text)
    d = datetime.datetime.now()
    db_ras_val(money=a, date=d)  # запись в БД с датой
    db_rashod_val(money=a)  # запись расхода в бд без даты
    b = balans
    c = b - a
    if c < 0:
        bot.send_message(message.chat.id, 'Недостаточно средств для списания.')
        return
    balans = c
    bot.send_message(message.chat.id, 'С карты списано: {k} рублей.'.format(k=message.text))
    bot.send_message(message.chat.id, f'Текущий баланс: {c:.2f} рублей.')
    db_balance_val(money=balans)


# Запускаем бота
bot.polling(none_stop=True, interval=0)  # чтобы ожидал ввода постоянно
