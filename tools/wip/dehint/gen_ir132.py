"""getImageSmc: unr_smc's job on t6 is only P(addr == 0x800) (the block after the sane test is aligned when branch > 4 * fallthru, i.e. the 3800 arm under ~2000): forms of the size arm, no unreachable."""
FOCUS = ['_getImageSmc']
BASE = 'tools/wip/dehint/drafts/image_read_attempt6.c'
src = open(BASE, newline='').read().replace('\r\n', '\n')
i = src.index('__attribute__((optimize("no-if-conversion", "no-if-conversion2", "no-tree-tail-merge"))) void getImageSmc')
j = src.index('void getImageKv(void)')
OLD = src[i:j]
LL = 'log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", addr);\n addr = 0x1000;\n'
S38 = 'log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3800\\n", size);\n'
S30 = 'log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3000\\n", size);\n'
REST = OLD[OLD.index('if (__builtin_expect(addr < 528 * xb.dumpPages, 0)) {'):]
REST = REST[:REST.index('	return;\nbad:')]
H = '''{
	struct flashhdr *h = (struct flashhdr *)xb.dump;
	int addr = SWAP32(h->smcBootAddr);
	int size = SWAP32(h->smcBootSize);
%s
'''
A3 = '__attribute__((optimize("no-if-conversion", "no-if-conversion2", "no-tree-tail-merge"))) '
PIN = '__asm__("" : "+D"(addr));'
Z = {'vh': f'if (!addr) {{ {LL} }} else {{ vhot: __attribute__((hot)); }}\n', 'v0': f'if (!addr) {{ {LL} }}\n'}
BL = {'bh': 'bhot: __attribute__((hot));\n', 'b0': ''}
T = 'unsigned t = addr;\n if (t != 0x1000) {{ if (t != 0x800) goto bad; }}\nbback:\n'
T = 'unsigned t = addr;\n if (t != 0x1000) { if (t != 0x800) goto bad; }\nbback:\n'
ARMS = {
 'eq': f'if (addr == 0x800) {{ size = 0x3800; {S38} }} else {{ size = 0x3000; {S30} }}',
 'ne': f'if (addr != 0x800) {{ size = 0x3000; {S30} }} else {{ size = 0x3800; {S38} }}',
 'ei10': f'if (addr == 0x800) {{ size = 0x3800; {S38} }} else if (addr == 0x1000) {{ size = 0x3000; {S30} }}',
 'ne10': f'if (addr != 0x1000) {{ size = 0x3800; {S38} }} else {{ size = 0x3000; {S30} }}',
 'eq10': f'if (addr == 0x1000) {{ size = 0x3000; {S30} }} else {{ size = 0x3800; {S38} }}',
 'sw': f'switch (addr) {{ case 0x800: size = 0x3800; {S38} break; default: size = 0x3000; {S30} break; }}',
 'sw2': f'switch (addr) {{ case 0x800: size = 0x3800; {S38} break; case 0x1000: size = 0x3000; {S30} break; }}',
 'sw3': f'switch (addr) {{ case 0x1000: size = 0x3000; {S30} break; default: size = 0x3800; {S38} break; }}',
 'pre': f'size = addr == 0x800 ? 0x3800 : 0x3000; if (addr == 0x800) {{ {S38} }} else {{ {S30} }}',
 'pre2': f'size = 0x3000; if (addr == 0x800) {{ size = 0x3800; {S38} }} else {{ {S30} }}',
 'pre3': f'size = 0x3800; if (addr == 0x800) {{ {S38} }} else {{ size = 0x3000; {S30} }}',
 'tst': f'if (addr == 0x800) size = 0x3800; else size = 0x3000; if (size == 0x3800) {{ {S38} }} else {{ {S30} }}',
 'tst2': f'if (addr == 0x800) size = 0x3800; else size = 0x3000; if (size != 0x3800) {{ {S30} }} else {{ {S38} }}',
 'gt': f'if (addr > 0x800) {{ size = 0x3000; {S30} }} else {{ size = 0x3800; {S38} }}',
 'le': f'if (addr <= 0x800) {{ size = 0x3800; {S38} }} else {{ size = 0x3000; {S30} }}',
 'lt': f'if (addr < 0x1000) {{ size = 0x3800; {S38} }} else {{ size = 0x3000; {S30} }}',
}
AX = []
for kz, z in Z.items():
    for kb, bl in BL.items():
        for ka, a in ARMS.items():
            tail = f'return;\nbad:\n{bl}{LL}goto bback;\n}}\n\n'
            AX.append(('.'.join((kz, kb, ka)), [(OLD, A3 + 'void getImageSmc(void)\n' + (H % '') + z + T + 'if (size != 0x3000 && size != 0x3800) { shot: __attribute__((hot));\n' + a + '} else {' + PIN + '}\n' + REST + tail)]))
AXES = [AX]
