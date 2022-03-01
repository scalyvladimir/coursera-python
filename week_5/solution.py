import socket
import time


class ClientError(Exception):
    """класс исключений клиента"""
    pass


MESSAGE_LEN = 1024


class Client:
    def __init__(self, address, port, timeout=None):
        self.sock = socket.create_connection((address, port), timeout)

    def put(self, metric_name, value, timestamp=None):
        if not timestamp:
            timestamp = int(time.time())

        request = 'put {} {} {}\n'.format(metric_name, value, timestamp)
        self.sock.send(request.encode('utf8'))
        answer = self.sock.recv(MESSAGE_LEN).decode('utf8').split('\n')

        if answer[0] != 'ok':
            raise ClientError

    def get(self, metric_name):
        request = 'get {}\n'.format(metric_name)
        self.sock.send(request.encode('utf8'))
        answer = self.sock.recv(MESSAGE_LEN).decode('utf8').split('\n')

        if answer[0] != 'ok':
            raise ClientError

        result = dict()
        for i in range(1, len(answer) - 2):
            temp = answer[i].split()

            if len(temp) != 3:
                raise ClientError
            metric_name = temp[0]

            try:
                metric_value = float(temp[1])
                timestamp = int(temp[2])
            except ValueError:
                raise ClientError

            record = tuple([timestamp, metric_value])
            if metric_name not in result:
                result[metric_name] = list()
            result[metric_name].append(record)

        for list_ in result.values():
            list_.sort(key=lambda x: x[0])

        return result

    def __del__(self):
        self.sock.close()
