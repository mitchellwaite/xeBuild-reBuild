"""getImageSmc: un gone via the switch's even odds (alignment right) with addr staying addr on the 3800 edge: switch on a converted copy so the PHI doesn't take 0x800 (no uncprop off a switch edge)."""
FOCUS = ['_getImageSmc']
BASE = 'tools/wip/dehint/drafts/image_read_attempt8.c'
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

'''
def at(*o):
    return '__attribute__((optimize(%s))) ' % ', '.join('"%s"' % x for x in o) if o else ''
I1, I2, TM = 'no-if-conversion', 'no-if-conversion2', 'no-tree-tail-merge'
ATTRS = {'a0': at(), 'tmi': at(TM, I2), 'i12': at(I1, I2), 'a3': at(I1, I2, TM)}
PIN = '__asm__("" : "+D"(addr));'
Z = {'vh': f'if (!addr) {{ {LL} }} else {{ vhot: __attribute__((hot)); }}\n', 'v0': f'if (!addr) {{ {LL} }}\n'}
BL = {'bh': 'bhot: __attribute__((hot));\n', 'b0': ''}
T = 'unsigned t = addr;\n if (t != 0x1000) { if (t != 0x800) goto bad; }\nbback:\n'
A38 = f'size = 0x3800; {S38}'
A30 = f'size = 0x3000; {S30}'
ARMS = {
 'u': f'switch ((unsigned)addr) {{ case 0x800: {A38} break; default: {A30} break; }}',
 'uv': f'unsigned u = addr; switch (u) {{ case 0x800: {A38} break; default: {A30} break; }}',
 'b4': f'switch (addr >> 11) {{ case 1: {A38} break; default: {A30} break; }}',
 'di': f'switch (addr - 0x800) {{ case 0: {A38} break; default: {A30} break; }}',
 'x8': f'switch (addr & 0x1800) {{ case 0x800: {A38} break; default: {A30} break; }}',
 'de': f'switch (addr == 0x800) {{ case 1: {A38} break; default: {A30} break; }}',
 'de0': f'switch (addr == 0x800) {{ case 0: {A30} break; default: {A38} break; }}',
 'el': f'switch (addr != 0x800) {{ case 0: {A38} break; default: {A30} break; }}',
}
AX = []
for kz, z in Z.items():
    for kb, bl in BL.items():
        for ka, a in ARMS.items():
            for kt, ta in ATTRS.items():
                for ks, sh in (('sh', 'shot: __attribute__((hot));\n'), ('s0', '')):
                    tail = f'return;\nbad:\n{bl}{LL}goto bback;\n}}\n\n'
                    AX.append(('.'.join((kz, kb, ka, kt, ks)), [(OLD, ta + 'void getImageSmc(void)\n' + H + z + T + 'if (size != 0x3000 && size != 0x3800) {' + sh + a + '} else {' + PIN + '}\n' + REST + tail)]))
AXES = [AX]
