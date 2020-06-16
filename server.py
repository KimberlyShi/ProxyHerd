import aiohttp
import asyncio
import json
import sys
import time
import re

url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
key = 'AIzaSyDSMmKARAlo8xG3PFlGh72kvoI7UQsV1Lk'
loop = ''
serverID = ''
allClients = {}
logFile = ''


portNums = {
    'Hill': 12235,
    'Jaquez': 12236,
    'Smith': 12237,
    'Campbell': 12238,
    'Singleton': 12239
}
"""
portNums = {
    'Hill': 8000,
    'Jaquez': 8001,
    'Smith': 8002,
    'Campbell': 8003,
    'Singleton': 8004
}
"""
possibleRoutes = {
    'Hill': ['Jaquez', 'Smith'],
    'Jaquez': ['Hill', 'Singleton'],
    'Smith': ['Hill', 'Campbell', 'Singleton'],
    'Campbell': ['Smith', 'Singleton'],
    'Singleton': ['Jaquez', 'Smith', 'Campbell']
}

#https://github.com/CS131-TA-team/UCLA_CS131_CodeHelp/blob/master/Python/echo_server.py
async def handle_echo(reader, writer):
    message = await reader.read(1000000)
    response, flag = await processCommands(message)
    try:
        if flag:
            writer.write(response.encode())
            await writer.drain()
        writer.close()
    except:
        log('ERROR: failed to write to server')

async def processCommands(message):
    message = message.decode() 
    entireMessage = message.replace('\n', '')
    entireMessage = re.sub(' +', '', entireMessage)
    entireMessage = message.strip().split()
    if entireMessage == 0:
        log('Received invalid command: {}'.format(message))
        response = '? {}'.format(message)
        return response, True
    command = entireMessage[0]
    secondArg = entireMessage[1]
    thirdArg = entireMessage[2]
    fourthArg = entireMessage[3]

    if command == 'IAMAT':
        if(len(entireMessage) != 4):
            log('Invalid: {}'.format(message))
            response = '? {}'.format(message)
            return response, True
        #secondArg = clientID, thirdArg = coords, fourthArg = timestamp
        latitudeStr, longitudeStr = findLatAndLong(thirdArg)
        if len(latitudeStr) > 0 and latitudeStr[0] == '-':
            latitudeStr = latitudeStr[1:]
        if len(longitudeStr) > 0 and longitudeStr[0] == '-':
            longitudeStr = longitudeStr[1:]
        if checkValidNum(fourthArg, 1) or \
            checkValidNum(latitudeStr, 1) or checkValidNum(longitudeStr, 1):
            log('ERROR: invalid value in IAMAT')
        else:
            lat = float(latitudeStr)
            lng = float(longitudeStr)
            if lat < -90 or lat > 90 or lng < -180 or lng > 180:
             log('ERROR: invalid coord in IAMAT')
            else:
                log('IAMAT: {}'.format(message))
                timeval = time.time() - float(fourthArg)
                timediff = str(timeval)
                if timeval >= 0.0:
                    timediff = '+' + timediff
                response = 'AT %s %s %s %s %s\n' % (serverID, timediff, secondArg, thirdArg, fourthArg)
                allClients[secondArg] = [serverID, timediff, secondArg, thirdArg, fourthArg]
                await propagate(response)
                return response, True

    elif command == 'WHATSAT':
        if(len(entireMessage) != 4):
            log('Invalid: {}'.format(message))
            response = '? {}'.format(message)
            return response, True
        #secondArg = client, thirdArg = radius, fourthArg = maxNumOfResults
        if checkValidNum(thirdArg, 0) or checkValidNum(fourthArg, 0) or \
        int(thirdArg) > 50 or int(thirdArg) < 0 or \
        int(fourthArg) > 20 or int(fourthArg) < 0 or \
        secondArg not in allClients:
            log('ERROR: Invalid info in WHATSAT')
        else:
            log('WHATSAT: {}'.format(message))
            radius = int(thirdArg) * 1000 #conversion
            max_results = int(fourthArg)
            lat, lng = findLatAndLong(allClients[secondArg][3])
            params = [('location', lat + ',' + lng), ('radius', str(radius)),('key', key)]
            #https://docs.aiohttp.org/en/stable/
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
                try:
                    async with session.get(url, params=params) as resp:
                        json_form = json.loads((await resp.text()))
                        json_form['results'] = json_form['results'][:max_results]
                        return ('AT %s %s %s %s %s\n' % (allClients[secondArg][0], allClients[secondArg][1], allClients[secondArg][2], allClients[secondArg][3], allClients[secondArg][4]) \
                            + json.dumps(json_form, indent=4) + '\n\n'), True
                except:
                    log('Request Failure')
                    return '? {}'.format(message), True
    elif command == 'AT':
        if(len(entireMessage) != 6):
            log('Invalid: {}'.format(message))
            response = '? {}'.format(message)
            return response, True
        log('AT: {}'.format(message))
       #secondArg = origin, thirdArg = timeDifference, fourthArg = client
        coords = entireMessage[4]
        timestamp = entireMessage[5]
        return await atCommand(message, secondArg, thirdArg, fourthArg, coords, timestamp), False
    
    log('Invalid: {}'.format(message))
    return '? {}'.format(message), True

async def atCommand(msg, origin, timediff, clientName, coords, timestamp):
    global allClients
    checkValid = True
    if clientName in allClients:
        if allClients[clientName] == [origin, timediff, clientName, coords, timestamp] or \
            allClients[clientName][4] > timestamp:
            checkValid = False
    if checkValid:
        log('new AT info: {}'.format(msg))
        allClients[clientName] = [origin, timediff, clientName, coords, timestamp]
        await propagate(msg)
    return None

#https://asyncio.readthedocs.io/en/latest/tcp_echo.html
async def propagate(msg):
    for x in possibleRoutes[serverID]:
        try:
            reader, writer = await asyncio.open_connection('127.0.0.1', portNums[x], loop=loop)
            writer.write(msg.encode())
            await writer.drain()
            writer.close()
        except:
            log('Failed to propagate to {}'.format(x))
            
def findLatAndLong(coords):
    if not coords[len(coords) - 1].isdigit() or \
        coords.count('+') + coords.count('-') != 2 or \
        coords[0] != '+' and coords[0] != '-':
        return None
    if coords[1:].find('+') == -1:
        finalCoord = coords[1:].split('-')
        if coords[0] == '+':
            return [finalCoord[0], '-' + finalCoord[1]]
        else:
            return ['-'+finalCoord[0], '-'+ finalCoord[1]]  
    else:
        finalCoord = coords[1:].split('+')
        if coords[0] == '+':
            return finalCoord
        else:
            finalCoord = ['-'+ finalCoord[0], finalCoord[1]]
            return finalCoord

def checkValidNum(inputArg, maxNum):
    num = 0
    if inputArg == '':
        return False
    for x in inputArg:
        if x == '.':
            num += 1
        if not x == '.' and not x.isdigit():
            return True
    if maxNum:
        return num > 1
    else:
        return num > 0
 
def log(message):
    if message == "":
        return
    try:
        logFile = open(serverID + '.txt', 'a')
        logFile.write(message + '\n')
        logFile.close()
    except:
        print('ERROR: failed to write to log')

def main():
    if len(sys.argv) != 2:
        sys.exit('ERROR: wrong number of args')
    global serverID, logFile, loop
    serverID = sys.argv[1]
    if serverID not in portNums:
        sys.exit('ERROR: Invalid server')
    else:
        logFile = open(serverID + '.txt', 'w')
        logFile.write('Opened server on port: ' + str(portNums[serverID]) + '\n')
        #https://asyncio.readthedocs.io/en/latest/tcp_echo.html
        loop = asyncio.get_event_loop()
        coro = asyncio.start_server(handle_echo, '127.0.0.1', portNums[serverID], loop=loop)
        server = loop.run_until_complete(coro)
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()

        logFile.close()
        log('Closed port: ' + str(portNums[serverID]) + '\n')
        sys.exit('Keyboard Interrupt')

if __name__ == '__main__':
    main()
