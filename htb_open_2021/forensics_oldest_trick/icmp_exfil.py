#!/usr/bin/env python3
from scapy.all import IP, ICMP, rdpcap

pcap = rdpcap('older_trick.pcap')

packets = []
for p in pcap:
    if ICMP in p:
        packets.append(p)

data = b''
for p in packets:
    if p[ICMP].type == 8:
        data += p.load[16:32]

with open('output.data', 'wb') as f:
    f.write(data)
