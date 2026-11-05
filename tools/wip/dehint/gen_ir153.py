"""getImageSmc: vhot's job (P(zero) under 15%) by opcode nonequal on the zero test: `z == 1` hidden from forwprop1 by a second use that fre1 folds.  Lattice of what else stays."""
FOCUS = ['_getImageSmc']
BASE = 'src/image_read.c'
src = open(BASE, newline='').read().replace('\r\n', '\n')
i = src.index('__attribute__((optimize("no-if-conversion", "no-if-conversion2", "no-tree-tail-merge"))) void getImageSmc')
j = src.index('void getImageKv(void)')
OLD = src[i:j]
LOG0 = 'log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", addr);\n'
LL = LOG0 + ' addr = 0x1000;\n'
S3800 = 'log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3800\\n", size);\n'
S3000 = 'log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3000\\n", size);\n'
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
ATTRS = {'a0': at(), 'tmi': at(TM, I2), 'a3': at(I1, I2, TM)}
PIN = '__asm__("" : "+D"(addr));'
Z = {
 'v0': f'if (!addr) {{ {LL} }}\n',
 'z1': f'int z = !addr; if (z == 1) {{ {LL} }}\n',
 'z5': f'int z = !addr; if (z == 1) {{ {LOG0} addr = 0x1000 * z; }}\n',
 'z6': f'int z = !addr; if (z == 1) {{ {LOG0} addr = z << 12; }}\n',
 'z7': f'int z = addr == 0; if (z == 1) {{ {LOG0} addr += 0x1000 * z; }}\n',
 'z8': f'int z = addr == 0; if (z != 1) ; else {{ {LOG0} addr += z << 12; }}\n',
 'p1': f'if (!(char *)addr) {{ {LL} }}\n',
 'p2': f'char *p = (char *)addr; if (!p) {{ {LL} }}\n',
 'p3': f'char *p = (char *)addr; if (p == 0) {{ {LOG0} addr = 0x1000; }}\n',
}
T = 'unsigned t = addr;\n if (t != 0x1000) { if (t != 0x800) goto bad; }\nbback:\n'
A38 = f'size = 0x3800; {S3800}'
A30 = f'size = 0x3000; {S3000}'
ARMS = {
 'if': f'if (addr == 0x800) {{ {A38} }} else {{ {A30} }}',
 'u': f'switch ((unsigned)addr) {{ case 0x800: {A38} break; default: {A30} break; }}',
}
AX = []
for kz, z in Z.items():
    for ka, a in ARMS.items():
        for kt, ta in ATTRS.items():
            for ks, sh in (('sh', 'shot: __attribute__((hot));\n'), ('s0', '')):
                tail = f'return;\nbad:\n{LL}goto bback;\n}}\n\n'
                AX.append(('.'.join((kz, ka, kt, ks)), [(OLD, ta + 'void getImageSmc(void)\n' + H + z + T + 'if (size != 0x3000 && size != 0x3800) {' + sh + a + '} else {' + PIN + '}\n' + REST + tail)]))
AXES = [AX]
