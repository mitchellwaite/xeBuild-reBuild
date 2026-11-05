"""getImageSmc 2-hint form: A is the tie around size's copy in the ok join (r104 <- r87 @ P(ok)): types and temporaries of size, load order; attribute a0 or tm."""
FOCUS = ['_getImageSmc']
BASE = 'tools/wip/dehint/drafts/image_read_attempt6.c'
src = open(BASE, newline='').read().replace('\r\n', '\n')
i = src.index('__attribute__((optimize("no-if-conversion", "no-if-conversion2", "no-tree-tail-merge"))) void getImageSmc')
j = src.index('void getImageKv(void)')
OLD = src[i:j]
LL = 'log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", addr);\n addr = 0x1000;\n'
S38 = 'log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3800\\n", size);\n'
S30 = 'log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3000\\n", size);\n'
ARM = f'if (addr == 0x800) {{ size = 0x3800; {S38} }} else {{ size = 0x3000; {S30} }}'
REST = OLD[OLD.index('if (__builtin_expect(addr < 528 * xb.dumpPages, 0)) {'):]
REST = REST[:REST.index('	return;\nbad:')]
def at(*o):
    return '__attribute__((optimize(%s))) ' % ', '.join('"%s"' % x for x in o) if o else ''
TM = 'no-tree-tail-merge'
ATTRS = {'a0': at(), 'tm': at(TM)}
PIN = '__asm__("" : "+D"(addr));'
Z = f'if (!addr) {{ {LL} }}\n'
T = 'unsigned t = addr;\n if (t != 0x1000) { if (t != 0x800) goto bad; }\nbback:\n'
HEADS = {
 'ii': 'int addr = SWAP32(h->smcBootAddr);\n int size = SWAP32(h->smcBootSize);',
 'iu': 'int addr = SWAP32(h->smcBootAddr);\n uint32_t size = SWAP32(h->smcBootSize);',
 'ul': 'int addr = SWAP32(h->smcBootAddr);\n unsigned long size = SWAP32(h->smcBootSize);',
 'il': 'int addr = SWAP32(h->smcBootAddr);\n long size = SWAP32(h->smcBootSize);',
 'st': 'int addr = SWAP32(h->smcBootAddr);\n uint32_t s = SWAP32(h->smcBootSize);\n int size = s;',
 'si': 'int addr = SWAP32(h->smcBootAddr);\n int s = SWAP32(h->smcBootSize);\n int size = s;',
 'su': 'int addr = SWAP32(h->smcBootAddr);\n int s = SWAP32(h->smcBootSize);\n uint32_t size = s;',
 'sd': 'int addr = SWAP32(h->smcBootAddr);\n int size;\n size = SWAP32(h->smcBootSize);',
 'r0': 'int size = SWAP32(h->smcBootSize);\n int addr = SWAP32(h->smcBootAddr);',
 'r1': 'uint32_t size = SWAP32(h->smcBootSize);\n int addr = SWAP32(h->smcBootAddr);',
}
AX = []
tail = f'return;\nbad:\n{LL}goto bback;\n}}\n\n'
for kh, hd in HEADS.items():
    for kc, cond in (('and', 'size != 0x3000 && size != 0x3800'), ('m3', '(size & 0xfffff7ff) != 0x3000')):
        for kt, ta in ATTRS.items():
            for kp, code in (('pe', f'if ({cond}) {{ {ARM} }} else {{ {PIN} }}'), ('pa', f'if ({cond}) {{ {ARM} }}\n {PIN}'), ('pn', f'if ({cond}) {{ {ARM} }}')):
                AX.append(('.'.join((kh, kc, kt, kp)), [(OLD, ta + 'void getImageSmc(void)\n{\n struct flashhdr *h = (struct flashhdr *)xb.dump;\n ' + hd + '\n' + Z + T + code + '\n' + REST + tail)]))
AXES = [AX]
