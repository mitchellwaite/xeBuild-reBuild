"""getImageSmc: exp_smc gone: the sane test under an outer test VRP folds.  The not-sane block has two predecessors, so no PRED_CALL on it; the sane block's freq is P(X) x 29%, band 18-22%."""
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
def at(*o):
    return '__attribute__((optimize(%s))) ' % ', '.join('"%s"' % x for x in o) if o else ''
I1, I2, TM = 'no-if-conversion', 'no-if-conversion2', 'no-tree-tail-merge'
ATTRS = {'a0': at(), 'tm': at(TM), 'a3': at(I1, I2, TM)}
PIN = '__asm__("" : "+D"(addr));'
Z = f'if (!addr) {{ {LL} }}\n'
T = 'unsigned t = addr;\n if (t != 0x1000) { if (t != 0x800) goto bad; }\nbback:\n'
A38 = f'size = 0x3800; {S3800}'
A30 = f'size = 0x3000; {S3000}'
ARM = f'if (addr == 0x800) {{ {A38} }} else {{ {A30} }}'
LIM = 'addr < 528 * xb.dumpPages'
XS = {'hh': 'h', 'sp': 'size > 0', 'sg': 'size >= 0x3000', 's0': 'size', 'sk': 'size != 0x4000', 'sk2': 'size != 0x8000', 'sl': 'size <= 0x3800', 'sm1': 'size != -1'}
FORMS = {
 'r1': lambda x: f'if ({x}) {{ if ({LIM}) {{ {SANE} return; }} }}\n {NOT}\n',
 'r2': lambda x: f'if ({x} && {LIM}) {{ {SANE} return; }}\n {NOT}\n',
 'n': lambda x: f'if ({x}) {{ if ({LIM}) {{ {SANE} goto done; }} }}\n {NOT}\n done:;\n',
 'aa': lambda x: f'if ({x} && {LIM}) {{ {SANE} }} else {{ {NOT} }}\n',
 'n2': lambda x: f'if ({LIM}) {{ if ({x}) {{ {SANE} goto done; }} }}\n {NOT}\n done:;\n',
}
AX = []
for kx, x in XS.items():
    for kf, f in FORMS.items():
        for kt, ta in ATTRS.items():
            tail = f'return;\nbad:\n{LL}goto bback;\n}}\n\n'
            AX.append(('.'.join((kx, kf, kt)), [(OLD, ta + 'void getImageSmc(void)\n' + H + Z + T + 'if (size != 0x3000 && size != 0x3800) {' + ARM + '} else {' + PIN + '}\n' + f(x) + tail)]))
AXES = [AX]
