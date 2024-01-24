import subprocess
import os
import re
from collections import namedtuple
import prettytable

def saved_ssids():
    wifis = subprocess.check_output('netsh wlan show profiles').decode()
    ssids = re.findall(r'All User Profile(.*)',wifis)
    wifi_names = []
    for ssid in ssids:
        wifi_names.append(ssid.strip().strip(':').strip())
    return wifi_names

def get_saved_passwords():
    profiles = []
    Profile = namedtuple('Profile', ['ssid','cipher','key'])
    for ssid in saved_ssids():
        info = subprocess.check_output(f"""netsh wlan show profile "{ssid}" key=clear""").decode()
        cipher = re.findall(r'Cipher\s(.*)',info)
        cipher = '/'.join([c.strip().strip(':').strip() for c in cipher])
        key = re.findall(r'Key Content\s(.*)',info)
        try:
            key = key[0].strip().strip(":").strip()
        except IndexError:
            key = "None"
        my_profile = Profile(ssid=ssid,cipher=cipher,key=key)
        profiles.append(my_profile)

    return profiles

table = prettytable.PrettyTable()
table.field_names = ['SSID', 'Cipher', 'Password']
for info in get_saved_passwords():
    table.add_row([info.ssid, info.cipher, info.key])

print(table)
