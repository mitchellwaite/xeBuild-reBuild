"""getImageSmc: shot and un both gone: a single-test size condition (72% nonequal) in place of the hot label.  Alignment wants P(size bad) * 28% under 20%."""
FOCUS = ['_getImageSmc']
BASE = 'tools/wip/dehint/drafts/image_read_attempt6.c'
src = open(BASE, newline='').read().replace('\r\n', '\n')
i = src.index('__attribute__((optimize("no-if-conversion", "no-if-conversion2", "no-tree-tail-merge"))) void getImageSmc')
j = src.index('void getImageKv(void)')
OLD = src[i:j]
LL = 'log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", addr);\n addr = 0x1000;\n'
S38 = 'log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3800\\n", size);\n'
S30 = 'log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3000\\n", size);\n'
A38 = 'size = 0x3800; ' + S38
A30 = 'size = 0x3000; ' + S30
REST = OLD[OLD.index('if (__builtin_expect(addr < 528 * xb.dumpPages, 0)) {'):]
REST = REST[:REST.index('	return;\nbad:')]
H = '''{
	struct flashhdr *h = (struct flashhdr *)xb.dump;
	int addr = SWAP32(h->smcBootAddr);
	int size = SWAP32(h->smcBootSize);
%s
'''
def at(*o):
    return '__attribute__((optimize(%s))) ' % ', '.join('"%s"' % x for x in o) if o else ''
I1, I2, TM = 'no-if-conversion', 'no-if-conversion2', 'no-tree-tail-merge'
ATTRS = {'a0': at(), 'i12': at(I1, I2), 'i1m': at(I1, TM), 'a3': at(I1, I2, TM)}
PIN = '__asm__("" : "+D"(addr));'
Z = {'vh': f'if (!addr) {{ {LL} }} else {{ vhot: __attribute__((hot)); }}\n', 'v0': f'if (!addr) {{ {LL} }}\n'}
BL = {'bh': 'bhot: __attribute__((hot));\n', 'b0': ''}
T = 'unsigned t = addr;\n if (t != 0x1000) { if (t != 0x800) goto bad; }\nbback:\n'
ARM = f'if (addr == 0x800) {{ {A38} }} else {{ {A30} }}'
UN = f'if (addr == 0x800) {{ {A38} }} else {{ size = 0x3000; if (!h) __builtin_unreachable(); {S30} }}'
CS = {'m1': '(size & ~0x800) != 0x3000', 'm2': '(size | 0x800) != 0x3800', 'm3': '(size & 0xfffff7ff) != 0x3000', 'm4': '(size - 0x3000 & ~0x800) != 0', 'm5': '(size - 0x3000) & ~0x800', 'm6': '(unsigned)(size & ~0x800) != 0x3000', 'and': 'size != 0x3000 && size != 0x3800'}
AX = []
for kz, z in Z.items():
    for kb, bl in BL.items():
        for kc, c in CS.items():
            for kt, ta in ATTRS.items():
                for ku, arm in (('u0', ARM), ('un', UN)):
                    for kp, e in (('noa', PIN), ('np', '')):
                        tail = f'return;\nbad:\n{bl}{LL}goto bback;\n}}\n\n'
                        AX.append(('.'.join((kz, kb, kc, kt, ku, kp)), [(OLD, ta + 'void getImageSmc(void)\n' + (H % '') + z + T + f'if ({c}) {{ {arm} }} else {{ {e} }}\n' + REST + tail)]))
AXES = [AX]
