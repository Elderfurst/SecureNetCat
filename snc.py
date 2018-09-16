# Written in Python 3.7.0
import argparse
import sys
import socket
import select

# Allow for the parsing of the correct command line arguments
parser = argparse.ArgumentParser(description='Secure Netcat')

parser.add_argument('-l', action='store_true')
parser.add_argument('--key')
parser.add_argument('destination')
parser.add_argument('port')

args = parser.parse_args()

# Read data from stdin
content = sys.stdin.read()

# Connect to the specified server and send the data
connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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