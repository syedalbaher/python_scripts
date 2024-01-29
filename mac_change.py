#!/bin/python3

import subprocess,re,argparse,os,sys

parser = argparse.ArgumentParser()
parser.add_argument('-i','--interface',help='Give it an inteface')
parser.add_argument('-n','--new',help='Give it a new mac address')
parser.add_argument('-r','--restore',help='Restore old mac address')
args = parser.parse_args()

new_mac = args.new
iface = args.interface

def get_mac(iface):
	ifconfig = subprocess.check_output(f'ifconfig {iface}',shell=True)
	pattern = r'ether\s((\d|[a-z]){2}:(\d|[a-z]){2}:(\d|[a-z]){2}:(\d|[a-z]){2}:(\d|[a-z]){2}:(\d|[a-z]){2})'
	mac = re.search(pattern,ifconfig.decode('utf-8'))
	return mac.group(1)

def change_mac(iface,new_mac):
	old_mac = get_mac(iface)
	try:
		subprocess.run(f'ifconfig {iface} down',shell=True)
		subprocess.run(f'ifconfig {iface} hw ether {new_mac}',shell=True)
		subprocess.run(f'ifconfig {iface} up',shell=True)
		print(f'NEW MAC {new_mac}')
	except Exception:
		print('Error Occured!')
		
		
if not args.restore:
	change_mac(iface,new_mac)
	if 'mac' not in os.listdir():
		with open('mac','x') as file:
			file.write(get_mac(iface))
else:
	if 'mac' in os.listdir():
		with open('mac','r') as file:
			new_mac_addr = file.read()
			change_mac(iface,new_mac_addr)
	else:
		print('First Spoof And Then Restore!<3')
