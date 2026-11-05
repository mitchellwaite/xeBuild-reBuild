"""getImageSmc: partial landing: t6 (vhot, bhot gone) + pin_addr kept, a or no a, attribute options, shot, unreachable."""
FOCUS = ['_getImageSmc']
BASE = 'tools/wip/dehint/drafts/image_read_attempt6.c'
src = open(BASE, newline='').read().replace('\r\n', '\n')
i = src.index('__attribute__((optimize("no-if-conversion", "no-if-conversion2", "no-tree-tail-merge"))) void getImageSmc')
j = src.index('void getImageKv(void)')
OLD = src[i:j]
L = 'log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", addr);\n addr = 0x1000;\n'
Z = f'if (!addr) {{ {L} }}\n'
S3800 = 'log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3800\\n", size);\n'
S3000 = 'log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3000\\n", size);\n'
REST = OLD[OLD.index('if (__builtin_expect(addr < 528 * xb.dumpPages, 0)) {'):]
REST = REST[:REST.index('	return;\nbad:')] + '}\n\n'
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
ATTRS = {'a0': '', 'tm': '__attribute__((optimize("no-tree-tail-merge"))) ', 'tmi': '__attribute__((optimize("no-tree-tail-merge", "no-if-conversion2"))) ',
         'i2': '__attribute__((optimize("no-if-conversion2"))) ', 'a3': '__attribute__((optimize("no-if-conversion", "no-if-conversion2", "no-tree-tail-merge"))) '}
AA = {'t6': Z + f'unsigned t = addr;\n if (t != 0x1000) {{ if (t != 0x800) {{ {L} }} }}\n',
      'and': Z + f'if (addr != 0x800 && addr != 0x1000) {{ {L} }}\n',}
PIN = '__asm__("" : "+D"(addr));'
def arm(un):
    u = 'if (!h) __builtin_unreachable();\n' if un else ''
    return f'if (addr == 0x800) {{ size = 0x3800; {S3800} }} else {{ size = 0x3000; {u} {S3000} }}'
AX = []
for ka, aa in AA.items():
    for kt, ta in ATTRS.items():
        for ks, sh in (('s0', ''), ('sh', 'shot: __attribute__((hot));\n')):
            for ku, un in (('u0', 0), ('un', 1)):
                for kn, decl, b, e, v in (('noa', '', '', PIN, 'addr'), ('k3', 'uint32_t a;', ' a = addr;', PIN + ' a = addr;', 'a')):
                    for kx, ex in (('ex', 1), ('e0', 0)):
                        AX.append(('.'.join((ka, kt, ks, ku, kn, kx)), [(OLD, ta + 'void getImageSmc(void)\n' + (H % decl) + aa + 'if (size != 0x3000 && size != 0x3800) {' + sh + arm(un) + b + '} else {' + e + '}\n' + rest(ex, v))]))
AXES = [AX]
