#!/usr/bin/env python3
from scapy.all import *

packets = rdpcap('dicts.pcapng')

for p in packets:
    s = p[Raw].load
#    print(s.hex())
    try:
        n = s.index(b'info_hash')
    except:
        continue
    info_hash = s[n+12:n+32].hex()
    print(info_hash)
