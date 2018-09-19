# Written in Python 3.7.0
import argparse
import sys
import socket
import select
import queue

# Allow for the parsing of the correct command line arguments
parser = argparse.ArgumentParser(description='Secure Netcat')

parser.add_argument('-l', action='store_true')
parser.add_argument('--key')
parser.add_argument('destination', nargs='?')
parser.add_argument('port')

args = parser.parse_args()

# Create the connection object
connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if bool(args.l):
    connection.bind(('0.0.0.0', int(args.port)))
    connection.listen(1)

    inputSources = [connection, sys.stdin]
    outputLocations = []
    outputData = {}

    incomingData = ''

    while inputSources:
        readable, writable, errors = select.select(inputSources, outputLocations, inputSources)
        for socket in readable:
            if socket is connection:
                clientConnection, clientAddress = socket.accept()
                inputSources.append(clientConnection)
                outputData[clientConnection] = queue.Queue()
            else:
                data = socket.recv(1024)
                if(data):
                    outputData[socket].put(data)
                    if socket not in outputLocations:
                        outputLocations.append(socket)
                else:
                    if socket in outputLocations:
                        outputLocations.remove(socket)
                    inputSources.remove(socket)
                    socket.close()
                    del outputData[socket]
        for socket in writable:
            try:
                nextMessage = outputData[socket].get_nowait()
            except queue.Empty:
                outputLocations.remove(socket)
            else:
                socket.send(nextMessage)
        for socket in errors:
            inputSources.remove(socket)
            if socket in outputLocations:
                outputLocations.remove(socket)
            socket.close()
            del outputData[socket]

# Read data from stdin
content = sys.stdin.read()

# Connect to the specified server and send the data
connection.connect((args.destination, int(args.port)))
connection.sendall(content)
connection.shutdown(socket.SHUT_WR)

# Read the data coming in if established as a listener
if bool(args.l):
    incoming = ''
    while True:
        newData = connection.recv(4096)
        if incoming == '':
            break
        else:
            incoming += newData

connection.close()
print(incoming)