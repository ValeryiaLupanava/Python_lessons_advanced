"""
Программа-клиент.
Функции клиента:
1. сформировать presence-сообщение;
2. отправить сообщение серверу;
3. получить ответ сервера;
4. разобрать сообщение сервера;
5. параметры командной строки скрипта client.py <addr> [<port>]:
    addr — ip-адрес сервера;
    port — tcp-порт на сервере, по умолчанию 7777.
"""

import sys
import json
import socket
import time
from common.variables import ACTION, PRESENCE, TIME, \
    USER, RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT, \
    NAME, SURNAME, HOST, IP_ADDRESS
from common.utils import get_message, send_message


def create_presence(account_name='Valeryia Lupanava'):
    '''
    Функция генерирует запрос о присутствии клиента
    :param account_name:
    :return:
    '''
    msg_to_server = {
        HOST: socket.gethostname(),
        IP_ADDRESS: socket.gethostbyname(socket.gethostname()),
        USER: {
            NAME: account_name.split(' ')[0],
            SURNAME: account_name.split(' ')[1]
        },
        ACTION: PRESENCE,
        TIME: time.time()
    }
    return msg_to_server


def process_ans(message):
    '''
    Функция разбирает ответ сервера
    :param message:
    :return:
    '''
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return f'200 : OK.\nHOST: {DEFAULT_IP_ADDRESS}.\nPORT: {DEFAULT_PORT}.'

        return f'400 : {message[ERROR]}'
    raise ValueError


def main():
    '''Загружаем параметы коммандной строки'''
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        server_address = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
    except ValueError:
        print('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    # Инициализация сокета и обмен

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.connect((server_address, server_port))
    message_to_server = create_presence()
    send_message(transport, message_to_server)
    try:
        answer = process_ans(get_message(transport))
        print(answer)
    except (ValueError, json.JSONDecodeError):
        print('Не удалось декодировать сообщение сервера.')


if __name__ == '__main__':
    main()
