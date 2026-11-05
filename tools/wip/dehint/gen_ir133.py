"""getImageSmc: the switch form of the size arm (gen_ir132 sw: vh, bh, un gone at 5 loose lines) against what's left: attribute subsets, shot, pin, a, expect, addr test forms, bad arm inline or at the end."""
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
def rest(ex, v):
    r = REST.replace('xb.dump + addr', 'xb.dump + ' + v)
    c = v + ' < 528 * xb.dumpPages'
    return r.replace('__builtin_expect(addr < 528 * xb.dumpPages, 0)', ('__builtin_expect(%s, 0)' % c) if ex else c)
H = '''{
	struct flashhdr *h = (struct flashhdr *)xb.dump;
	int addr = SWAP32(h->smcBootAddr);
	int size = SWAP32(h->smcBootSize);
%s
'''
def at(*o):
    return '__attribute__((optimize(%s))) ' % ', '.join('"%s"' % x for x in o) if o else ''
I1, I2, TM = 'no-if-conversion', 'no-if-conversion2', 'no-tree-tail-merge'
ATTRS = {'a0': at(), 'i1': at(I1), 'i2': at(I2), 'tm': at(TM), 'i12': at(I1, I2), 'i1m': at(I1, TM), 'tmi': at(TM, I2), 'a3': at(I1, I2, TM)}
PIN = '__asm__("" : "+D"(addr));'
Z = f'if (!addr) {{ {LL} }}\n'
SW = f'switch (addr) {{ case 0x800: size = 0x3800; {S38} break; default: size = 0x3000; {S30} break; }}'
AX = []
for kaa, tg, ti in (('t6', 'unsigned t = addr;\n if (t != 0x1000) { if (t != 0x800) goto bad; }\nbback:\n', 'unsigned t = addr;\n if (t != 0x1000) { if (t != 0x800) { %s } }\n'),
                    ('and', 'if (addr != 0x800 && addr != 0x1000) goto bad;\nbback:\n', 'if (addr != 0x800 && addr != 0x1000) { %s }\n')):
    for kk, inline in (('en', 0), ('in', 1)):
        aa = Z + ((ti % LL) if inline else tg)
        tail = '}\n\n' if inline else f'return;\nbad:\n{LL}goto bback;\n}}\n\n'
        for kt, ta in ATTRS.items():
            for ks, sh in (('s0', ''), ('sh', 'shot: __attribute__((hot));\n')):
                for kn, decl, b, e, v in (('noa', '', '', PIN, 'addr'), ('np', 'uint32_t a;', ' a = addr;', ' a = addr;', 'a')):
                    for kx, ex in (('ex', 1), ('e0', 0)):
                        AX.append(('.'.join((kaa, kk, kt, ks, kn, kx)), [(OLD, ta + 'void getImageSmc(void)\n' + (H % decl) + aa + 'if (size != 0x3000 && size != 0x3800) {' + sh + SW + b + '} else {' + e + '}\n' + rest(ex, v) + tail)]))
AXES = [AX]
