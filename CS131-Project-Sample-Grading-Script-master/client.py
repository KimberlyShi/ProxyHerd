import asyncio
import sys
import time

loop = ''
max_msg_len = 1e6

"""
server_dict = {
    'Hill': 12235,
    'Jaquez': 12236,
    'Smith': 12237,
    'Campbell': 12238,
    'Singleton': 12239
}

"""
server_dict = {
    'Hill': 8000,
    'Jaquez': 8001,
    'Smith': 8002,
    'Campbell': 8003,
    'Singleton': 8004
}

test_messages = ["WHATSAT kiwi.cs.ucla.edu 1- 5 "]

#inspo from https://github.com/CS131-TA-team/UCLA_CS131_CodeHelp/blob/master/Python/echo_client.py
async def write_mesg(message):
    reader, writer = await asyncio.open_connection('127.0.0.1', server_dict['Singleton'], loop=loop)
    print('Sent: {}'.format(message))
    writer.write(message.encode())
    data = await reader.read(max_msg_len)
    #response = data.decode()
    print('Received: {}'.format(data.decode()))
    writer.close()

def main():
        global loop
        loop = asyncio.get_event_loop()
        loop.run_until_complete(write_mesg(test_messages[0] + '\n'))
        loop.close()

if __name__ == '__main__':
    main()