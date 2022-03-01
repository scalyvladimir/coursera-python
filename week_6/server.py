import asyncio


def run_server(host, port):
    buffer = dict()

    class ClientServerProtocol(asyncio.Protocol):
        def connection_made(self, transport):
            self.transport = transport

        def process_data(self, data):
            result = 'ok'

            if data.count(' ') < 1:
                return 'error\nwrong command\n\n'

            request, data = data.split(' ', 1)

            if not data.endswith('\n') or data.count('\n') != 1:
                result = 'error\nwrong command'

            else:
                data = data.strip('\n ')

            data_list = data.split()

            if request not in ['get', 'put'] or data == '':
                result = 'error\nwrong command'

            elif request == 'get':
                if len(data_list) != 1:
                    result = 'error\nwrong command'
                elif data in buffer.keys():
                    for metric_tup in buffer[data]:
                        str_list = [str(x) for x in metric_tup]
                        result += f'\n{data} ' + ' '.join(str_list)
                elif data == '*':
                    for key in buffer.keys():
                        temp = ''
                        for metric_tup in buffer[key]:
                            str_list = [str(x) for x in metric_tup]
                            temp += f'\n{key} ' + ' '.join(str_list)
                        result += temp

            elif request == 'put':
                if len(data_list) != 3:
                    result = 'error\nwrong command'
                else:
                    metric_name, metric_val, timestamp = data_list
                    try:
                        metric_val, timestamp = float(metric_val), int(timestamp)
                        if metric_name not in buffer.keys():
                            buffer[metric_name] = []

                        record = [metric_val, timestamp]

                        is_found = False
                        for id, tup in enumerate(buffer[metric_name]):
                            item_list = list(tup)

                            if item_list[1] == timestamp:
                                item_list[0] = metric_val
                                is_found = True

                            buffer[metric_name][id] = tuple(item_list)

                        if not is_found:
                            buffer[metric_name].append(tuple(record))

                    except ValueError:
                        result = 'error\nwrong command'

            return f'{result}\n\n'

        def data_received(self, data):
            resp = self.process_data(data.decode())
            self.transport.write(resp.encode())

    loop = asyncio.get_event_loop()

    coro = loop.create_server(
        protocol_factory=ClientServerProtocol,
        host=host, port=port
    )

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

# run_server('127.0.0.1', 8888)
