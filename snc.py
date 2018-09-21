# Written in Python 3.7.0
import argparse
import sys
import socket
import select
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes

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

    try:
        while True:
            for socket in select.select(inputSources, [], [])[0]:
                # This means a new connection has been received
                if socket is connection:
                    clientConnection, clientAddress = socket.accept()
                    inputSources.append(clientConnection)
                # sys.stdin is the current readable source
                elif socket is sys.stdin:
                    data = socket.readline()
                    # TODO Encrypt message here
                    encryptedData = data
                    for source in inputSources:
                        if source not in [sys.stdin, connection]:
                            source.sendall(encryptedData.encode('utf-8'))
                # An actual client connection is the source
                else:
                    data = socket.recv(1024)
                    if data:
                        # TODO Decrypt message here
                        decryptedData = data
                        sys.stdout.write(decryptedData.decode('utf-8'))
                    else:
                        inputSources.remove(socket)
                        socket.close()
                        connection.close()
                        exit(0)
    except KeyboardInterrupt:
        connection.close()
        exit(0)
else:
    try:
        connection.connect((args.destination, int(args.port)))
        inputSources = [sys.stdin, connection]
        while True:
            for socket in select.select(inputSources, [], [])[0]:
                # Read the data coming from stdin
                if socket is sys.stdin:
                    data = socket.readline()
                    if data:
                        # TODO Encrypt message here
                        encryptedData = data
                        connection.sendall(encryptedData.encode('utf-8'))
                    else:
                        connection.close()
                        exit(0)
                # Receive the data from the server
                else:
                    data = connection.recv(1024)
                    # TODO decrypt data here
                    decryptedData = data
                    sys.stdout.write(decryptedData.decode('utf-8'))
                    inputSources.remove(connection)
    except KeyboardInterrupt:
        connection.close()
        exit(0)