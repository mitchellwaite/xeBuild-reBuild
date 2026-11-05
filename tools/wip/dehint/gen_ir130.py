"""getImageSmc: as gen_ir129 but the bad arm at the end of the function behind a goto (as in src), and the source's shape with hint subsets; a or no a; with/without t6."""
FOCUS = ['_getImageSmc']
BASE = 'tools/wip/dehint/drafts/image_read_attempt6.c'
src = open(BASE, newline='').read().replace('\r\n', '\n')
i = src.index('__attribute__((optimize("no-if-conversion", "no-if-conversion2", "no-tree-tail-merge"))) void getImageSmc')
j = src.index('void getImageKv(void)')
OLD = src[i:j]
LL = 'log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", addr);\n addr = 0x1000;\n'
S3800 = 'log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3800\\n", size);\n'
S3000 = 'log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3000\\n", size);\n'
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
ATTRS = {'a0': '', 'tm': '__attribute__((optimize("no-tree-tail-merge"))) ', 'i2': '__attribute__((optimize("no-if-conversion2"))) ',
         'tmi': '__attribute__((optimize("no-tree-tail-merge", "no-if-conversion2"))) '}
PIN = '__asm__("" : "+D"(addr));'
def arm(un):
    u = 'if (!h) __builtin_unreachable();\n' if un else ''
    return f'if (addr == 0x800) {{ size = 0x3800; {S3800} }} else {{ size = 0x3000; {u} {S3000} }}'
AX = []
for kz, z in (('v0', f'if (!addr) {{ {LL} }}\n'), ('vh', f'if (!addr) {{ {LL} }} else {{ vhot: __attribute__((hot)); }}\n')):
    for kb, bl in (('b0', ''), ('bh', 'bhot: __attribute__((hot));\n')):
        for kaa, tests in (('t6', 'unsigned t = addr;\n if (t != 0x1000) {{ if (t != 0x800) goto bad; }}\nbback:\n'),
                           ('and', 'if (addr != 0x800 && addr != 0x1000) goto bad;\nbback:\n'),):
            aa = z + tests
            tail = f'return;\nbad:\n{bl}{LL}goto bback;\n}}\n\n'
            for kt, ta in ATTRS.items():
                for ks, sh in (('s0', ''), ('sh', 'shot: __attribute__((hot));\n')):
                    for ku, un in (('u0', 0), ('un', 1)):
                        for kn, decl, b, e, v in (('noa', '', '', PIN, 'addr'), ('k3', 'uint32_t a;', ' a = addr;', PIN + ' a = addr;', 'a'),
                                                  ('np', 'uint32_t a;', ' a = addr;', ' a = addr;', 'a')):
                            for kx, ex in (('ex', 1), ('e0', 0)):
                                AX.append(('.'.join((kz, kb, kaa, kt, ks, ku, kn, kx)), [(OLD, ta + 'void getImageSmc(void)\n' + (H % decl) + aa + 'if (size != 0x3000 && size != 0x3800) {' + sh + arm(un) + b + '} else {' + e + '}\n' + rest(ex, v) + tail)]))
AXES = [AX]
