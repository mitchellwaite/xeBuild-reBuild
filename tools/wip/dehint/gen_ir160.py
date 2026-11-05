"""getImageSmc: hint lattice around gen_ir155's near miss, for a partial landing.  Labels: sane form, attribute, then hints that stay."""
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
ATTRS = {'a0': at(), 'tm': at(TM), 'i2': at(I2), 'tmi': at(TM, I2), 'a3': at(I1, I2, TM), 'i1m': at(I1, TM), 'i12': at(I1, I2), 'i1': at(I1)}
PIN = '__asm__("" : "+D"(addr));'
LIM = 'addr < 528 * xb.dumpPages'
HF = 'static void loadSmc(int addr, int size)\n{\n' + SANE + '}\n\n'
FORMS = {
 'xh': (HF, f'if (t && {LIM}) {{ loadSmc(addr, size); }} else {{ {NOT} }}\n'),
 'xn': ('', f'if (t && {LIM}) {{ {SANE} }} else {{ {NOT} }}\n'),
 'hx': (HF, f'if (__builtin_expect({LIM}, 0)) {{ loadSmc(addr, size); }} else {{ {NOT} }}\n'),
 'ex': ('', f'if (__builtin_expect({LIM}, 0)) {{ {SANE} }} else {{ {NOT} }}\n'),
}
T = 'unsigned t = addr;\n if (t != 0x1000) { if (t != 0x800) goto bad; }\nbback:\n'
AX = []
for kf, (hf, sa) in FORMS.items():
    for kq, q in ATTRS.items():
        for vh in (0, 1):
            for bh in (0, 1):
                for sh in (0, 1):
                    for un in (0, 1):
                        z = f'if (!addr) {{ {LL} }}' + (' else { vhot: __attribute__((hot)); }\n' if vh else '\n')
                        u = 'if (!h) __builtin_unreachable();\n' if un else ''
                        arm = f'if (addr == 0x800) {{ size = 0x3800; {S3800} }} else {{ size = 0x3000; {u} {S3000} }}'
                        lab = '.'.join([kf, kq] + [n for n, v in (('vh', vh), ('bh', bh), ('sh', sh), ('un', un)) if v])
                        tail = 'return;\nbad:\n' + ('bhot: __attribute__((hot));\n' if bh else '') + LL + 'goto bback;\n}\n\n'
                        AX.append((lab, [(OLD, hf + q + 'void getImageSmc(void)\n' + H + z + T + 'if (size != 0x3000 && size != 0x3800) {' + ('shot: __attribute__((hot));\n' if sh else '') + arm + '} else {' + PIN + '}\n' + sa + tail)]))
AXES = [AX]
