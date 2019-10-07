
from time import time
import socket


class ClientError(Exception):
    def __init__(self, errortext=None):
        self.errortext = errortext


class Client:

    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout

    def put(self, key, value, timestamp=int(time())):
        sock = socket.create_connection(('127.0.0.1', 10001), timeout=self.timeout)
        msg = 'put' + ' ' + key + ' ' + str(value) + ' ' + str(timestamp) + '\n'
        sock.send(bytes(msg, encoding='utf-8'))
        try:
            data = sock.recv(1024)
            responce = data.decode('utf-8')
        except socket.timeout:
            print('TimeoutError')
            responce = None
        if responce == 'error\nwrong command\n\n':
            raise ClientError('Ошибка сервера!')
        print(responce)

    def get(self, key):
        sock = socket.create_connection((self.host, self.port), timeout=self.timeout)
        msg = 'get' + ' ' + key + '\n'
        sock.send(bytes(msg, encoding='utf-8'))
        try:
            data = sock.recv(1024)
            responce = [data.decode('utf-8')]
            print(responce)
        except socket.timeout:
            print('TimeoutError')
            responce = None
        if responce[0] == 'ok\n\n':
            return {}
        elif responce[0][0:2] != 'ok':
            raise ClientError('Ошибка сервера!')
        else:
            dict = {}
            responce = str(responce)[6:-1][:-1][:-1][:-1][:-1][:-1]
            responce_lst = responce.split('\\n')
            for i in responce_lst:
                lst = i.split()
                cort = (int(lst[2]), float(lst[1]))
                if lst[0] not in dict:
                    dict[lst[0]] = [cort]
                else:
                    dict[lst[0]].append(cort)
            for i in dict:
                dict[i] = sorted(dict[i], key=lambda tpl: tpl[1], reverse=True)
        return dict
