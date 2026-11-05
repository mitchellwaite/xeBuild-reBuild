"""getImageSmc: gen_ir117's k3 (a real uint32_t a set in the size test's arms) with forms of the addr test that give P(bad) over 50%."""
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
def rest(ex):
    r = REST.replace('xb.dump + addr', 'xb.dump + a')
    c = 'a < 528 * xb.dumpPages'
    return r.replace('__builtin_expect(addr < 528 * xb.dumpPages, 0)', ('__builtin_expect(%s, 0)' % c) if ex else c)
INT = '''void getImageSmc(void)
{
	struct flashhdr *h = (struct flashhdr *)xb.dump;
	int addr = SWAP32(h->smcBootAddr);
	int size = SWAP32(h->smcBootSize);
	uint32_t a;

'''
AD = {
    'and': Z + f'if (addr != 0x800 && addr != 0x1000) {{ {L} }}\n',
    't1': Z + f'uint32_t t = addr;\n if (t != 0x800) {{ if (t != 0x1000) {{ {L} }} }}\n',
    't1b': Z + f'{{ uint32_t t = addr;\n if (t != 0x800) {{ if (t != 0x1000) {{ {L} }} }} }}\n',
    't2': Z + f'if ((uint32_t)addr != 0x800) {{ if ((uint32_t)addr != 0x1000) {{ {L} }} }}\n',
    't4': Z + f'if (addr != 0x800) {{ if (addr != 0x1000) {{ {L} }} }}\n',
    't5': Z + f'a = addr;\n if (a != 0x800) {{ if (a != 0x1000) {{ {L} }} }}\n',
    't6': Z + f'unsigned t = addr;\n if (t != 0x1000) {{ if (t != 0x800) {{ {L} }} }}\n',
}
def test(body, els, p):
    if p == 'and':
        return 'if (size != 0x3000 && size != 0x3800) {%s} else {%s}\n' % (body, els)
    if p == 'cmask':
        return 'if ((size & ~0x800) != 0x3000) {%s} else {%s}\n' % (body, els)
    if p == 'rev':
        return 'if (size == 0x3000 || size == 0x3800) {%s} else {%s}\n' % (els, body)
def sizes(kind, p):
    if kind == 'k3':
        return test(f'if (addr == 0x800) {{ size = 0x3800; {S3800} }} else {{ size = 0x3000; {S3000} }} a = addr;', 'a = addr;', p)
    if kind == 'k6':
        return test(f'if (addr == 0x800) {{ size = 0x3800; {S3800} a = 0x800; }} else {{ size = 0x3000; {S3000} a = addr; }}', 'a = addr;', p)
AX = []
for ka, aa in AD.items():
    for p in ('and', 'cmask', 'rev'):
        for k in ('k3', 'k6'):
            for ex in (1, 0):
                AX.append(('.'.join((ka, p, k, 'ex' if ex else 'e0')), [(OLD, INT + aa + sizes(k, p) + rest(ex))]))
AXES = [AX]
