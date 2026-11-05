"""getImageSmc: the sane arm in a static helper (a call + return at profile_estimate, so call 29 and early return 39 on it: 20.7%, under an outer test VRP folds)."""
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
a = REST.index('{') + 1
b = REST.rindex('} else {')
SANE = REST[a:b]
NOT = REST[b + len('} else {'):REST.rindex('}')]
H = '''{
	struct flashhdr *h = (struct flashhdr *)xb.dump;
	int addr = SWAP32(h->smcBootAddr);
	int size = SWAP32(h->smcBootSize);

'''
PIN = '__asm__("" : "+D"(addr));'
Z = f'if (!addr) {{ {LL} }}\n'
A38 = f'size = 0x3800; {S3800}'
A30 = f'size = 0x3000; {S3000}'
ARM = f'if (addr == 0x800) {{ {A38} }} else {{ {A30} }}'
LIM = 'addr < 528 * xb.dumpPages'
TS = {
 'en': ('unsigned t = addr;\n if (t != 0x1000) { if (t != 0x800) goto bad; }\nbback:\n', f'return;\nbad:\n{LL}goto bback;\n'),
 'in': (f'unsigned t = addr;\n if (t != 0x1000) {{ if (t != 0x800) {{ {LL} }} }}\n', ''),
 'gd': ('unsigned t = addr;\n if (t != 0x1000) { if (t != 0x800) goto bad; }\nbback:\n', f'goto done;\nbad:\n{LL}goto bback;\ndone:;\n'),
}
HELP = {
 'ii': ('static void loadSmc(int addr, int size)\n{\n' + SANE + '}\n\n', 'loadSmc(addr, size);'),
 'uu': ('static void loadSmc(uint32_t addr, uint32_t size)\n{\n' + SANE + '}\n\n', 'loadSmc(addr, size);'),
}
XS = {'tt': 't'}
HELP['nh'] = ('', SANE)
def at(*o):
    return '__attribute__((optimize(%s))) ' % ', '.join('"%s"' % x for x in o) if o else ''
I1, I2, TM = 'no-if-conversion', 'no-if-conversion2', 'no-tree-tail-merge'
ATTRS = {'a0': at(), 'tm': at(TM), 'i2': at(I2), 'tmi': at(TM, I2), 'a3': at(I1, I2, TM)}
FORMS = {
 'r': lambda x, c: f'if ({x}) {{ if ({LIM}) {{ {c} return; }} }}\n {NOT}\n',
 'g': lambda x, c: f'if ({x} && {LIM}) {{ {c} }} else {{ {NOT} }}\n',
}
AX = []
for kh, (hf, c) in HELP.items():
    for kt, (ta, tb) in TS.items():
        for kx, x in XS.items():
            for kf, f in FORMS.items():
                for kq, q in ATTRS.items():
                    AX.append(('.'.join((kh, kt, kx, kf, kq)), [(OLD, hf + q + 'void getImageSmc(void)\n' + H + Z + ta + 'if (size != 0x3000 && size != 0x3800) {' + ARM + '} else {' + PIN + '}\n' + f(x, c) + tb + '}\n\n')]))
AXES = [AX]
