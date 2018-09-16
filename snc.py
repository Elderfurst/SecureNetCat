# Written in Python 3.7.0

import argparse

# Allow for the parsing of the correct command line arguments

parser = argparse.ArgumentParser(description='Secure NetCat')

parser.add_argument('-l', action='store_true')
parser.add_argument('--key')
parser.add_argument('destination')
parser.add_argument('port')

args = parser.parse_args()

print(args)