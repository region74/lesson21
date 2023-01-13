import requests
import pprint
import time

TOKEN = '5914159692:AAHEr0XfUxEeryUovHjmHO-x3WDuy13a-r4'
MAIN_URL = f'https://api.telegram.org/bot{TOKEN}'

proxies = {
    'http': 'http://195.245.221.37:80',
    'https': 'http://195.245.221.37:80'
}

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
}

# Информация о боте
url = f'{MAIN_URL}/getMe'
result = requests.get(url)
pprint.pprint(result.json())

# Попытки с прокси
# result = requests.get(url,headers=headers)
# result = requests.get(url, proxies=proxies, headers=headers)


# как понять что есть вхоядщее смс
# получение обновлений
while True:
    time.sleep(5)
    url = f'{MAIN_URL}/getUpdates'
    result = requests.get(url)
    pprint.pprint(result.json())

    # как ответить на сообщение

    messages = result.json()['result']
    for message in messages:
        chat_id = message['message']['chat']['id']
        url = f'{MAIN_URL}/sendMessage'
        params = {
            'chat_id': chat_id,
            'text': 'Привет'
        }
        result = requests.post(url, params=params)
