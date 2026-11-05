"""getImageSmc hint-free: the reference's join (bb10: `ebx = (unsigned)edi`) must exist as a statement in the size test's ok path.
Two real variables: int addr for the logs, uint32_t a for the arithmetic, assigned at several places."""
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
INT = '''void getImageSmc(void)
{
	struct flashhdr *h = (struct flashhdr *)xb.dump;
	int addr = SWAP32(h->smcBootAddr);
	int size = SWAP32(h->smcBootSize);
	uint32_t a;

'''
ISZ = '''void getImageSmc(void)
{
	struct flashhdr *h = (struct flashhdr *)xb.dump;
	int addr = SWAP32(h->smcBootAddr);
	int s = SWAP32(h->smcBootSize);
	uint32_t size = s;
	uint32_t a;

'''
AD = {
    'n': Z + f'a = addr;\n if (a != 0x800) {{ if (a != 0x1000) {{ {L} }} }}\n',
    'n2': Z + f'if ((a = addr) != 0x800) {{ if (a != 0x1000) {{ {L} a = addr; }} }}\n',
    'b': Z + f'if (addr != 0x800 && addr != 0x1000) {{ {L} }}\n',
}
SF = {
    'and': (INT, 'size != 0x3000 && size != 0x3800'),
    'nest': (ISZ, None),
}
def sizes(sf, kind):
    test = lambda body, els: (('if (size != 0x3000 && size != 0x3800) {%s} else {%s}\n' % (body, els)) if sf == 'and'
                              else ('if (s != 0x3000) { if (s != 0x3800) {%s} else {%s} } else {%s}\n' % (body, els, els)))
    if kind == 'k1':  # a before the test
        return 'a = addr;\n' + test(f'if (addr == 0x800) {{ size = 0x3800; {S3800} }} else {{ size = 0x3000; {S3000} }}', '')
    if kind == 'k3':  # a in every arm
        return test(f'if (addr == 0x800) {{ size = 0x3800; {S3800} }} else {{ size = 0x3000; {S3000} }} a = addr;', 'a = addr;')
    if kind == 'k4':  # in the arms
        return test(f'if (addr == 0x800) {{ size = 0x3800; {S3800} a = addr; }} else {{ size = 0x3000; {S3000} a = addr; }}', 'a = addr;')
    if kind == 'k5':  # after
        return test(f'if (addr == 0x800) {{ size = 0x3800; {S3800} }} else {{ size = 0x3000; {S3000} }}', '') + 'a = addr;\n'
    if kind == 'k6':  # constants in the arms
        return test(f'if (addr == 0x800) {{ size = 0x3800; {S3800} a = 0x800; }} else {{ size = 0x3000; {S3000} a = addr; }}', 'a = addr;')
AX = []
for ka, aa in AD.items():
    for sf, (h, _) in SF.items():
        for k in ('k1', 'k3', 'k4', 'k5', 'k6'):
            for kv in ('a', 'addr'):
                for ex in (1, 0):
                    AX.append(('.'.join((ka, sf, k, kv, 'ex' if ex else 'e0')), [(OLD, h + aa + sizes(sf, k) + rest(ex, kv))]))
AXES = [AX]
