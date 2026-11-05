"""getImageSmc: as gen_ir139, size's test nested so VRP knows size on the ok path (`size > 0` folds, 64% x 29% = 18.6%), and nested size P 51.8% for the bb-reorder tie."""
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
R0 = OLD[OLD.index('if (__builtin_expect(addr < 528 * xb.dumpPages, 0)) {'):]
R0 = R0[:R0.index('	return;\nbad:')]
SANE = R0[R0.index('{') + 1:R0.index('} else {\n\t\tlog_printf(1, "SMC at')]
NS = 'log_printf(1, "SMC at 0x%x of size 0x%x is not sane, skipping smc.bin in NAND image\\n", addr, size);\n'
def at(*o):
    return '__attribute__((optimize(%s))) ' % ', '.join('"%s"' % x for x in o) if o else ''
I2, TM = 'no-if-conversion2', 'no-tree-tail-merge'
ATTRS = {'a0': at(), 'tm': at(TM), 'tmi': at(TM, I2)}
PIN = '__asm__("" : "+D"(addr));'
Z = f'if (!addr) {{ {LL} }}\n'
T = 'unsigned t = addr;\n if (t != 0x1000) { if (t != 0x800) goto bad; }\nbback:\n'
C = 'addr < 528 * xb.dumpPages'
HEAD = {'int': 'int size = SWAP32(h->smcBootSize);', 'iu': 'int s = SWAP32(h->smcBootSize);\n uint32_t us = s;\n int size = s;'}
SIZE = {
 'nsi': ('int', f'if (size != 0x3000) {{ if (size != 0x3800) {{ {ARM} goto sized; }} }} {PIN} sized:\n'),
 'nsi8': ('int', f'if (size != 0x3800) {{ if (size != 0x3000) {{ {ARM} goto sized; }} }} {PIN} sized:\n'),
 'nsu': ('iu', f'if (us != 0x3000) {{ if (us != 0x3800) {{ {ARM} goto sized; }} }} {PIN} sized:\n'),
 'nsu8': ('iu', f'if (us != 0x3800) {{ if (us != 0x3000) {{ {ARM} goto sized; }} }} {PIN} sized:\n'),
 'and': ('int', f'if (size != 0x3000 && size != 0x3800) {{ {ARM} }} else {{ {PIN} }}\n'),
}
AX = []
tail = f'return;\nbad:\n{LL}goto bback;\n}}\n\n'
for ks, (kh, code) in SIZE.items():
    for ko, o in {'sgt': 'size > 0', 'sne': 'size', 'sge': 'size >= 0'}.items():
        f = f'if ({o}) {{ if ({C}) {{ {SANE} goto done; }} }}\n {NS} done:;\n'
        for kt, ta in ATTRS.items():
            AX.append(('.'.join((ks, ko, kt)), [(OLD, ta + 'void getImageSmc(void)\n{\n struct flashhdr *h = (struct flashhdr *)xb.dump;\n int addr = SWAP32(h->smcBootAddr);\n ' + HEAD[kh] + '\n' + Z + T + code + f + tail)]))
AXES = [AX]
