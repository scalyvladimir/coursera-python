from __init__ import *
import asyncio


def test():
    async def echo(reader, writer):
        data = await reader.read(MESSAGE_LEN)
        msg = data.decode()
        addr = writer.get_extra_info('peername')
        print('received {} from {}'.format(msg, addr))
        writer.close()

    loop = asyncio.get_event_loop()

    coro = asyncio.start_server(echo, IP_ADDRESS, PORT, loop=loop)

    server = loop.run_until_complete(coro)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print('Goodbye!')

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


print('\n'.rstrip('\n') == '')