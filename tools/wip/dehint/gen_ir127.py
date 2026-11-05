"""getImageSmc: t6 and a real a, size nested on int s with uint32_t size (merges, P 51.8), or forms to raise P(size bad) a little."""
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
HI = '''void getImageSmc(void)
{
	struct flashhdr *h = (struct flashhdr *)xb.dump;
	int addr = SWAP32(h->smcBootAddr);
	int s = SWAP32(h->smcBootSize);
	uint32_t size = s;
	uint32_t a;

'''
HR = '''void getImageSmc(void)
{
	struct flashhdr *h = (struct flashhdr *)xb.dump;
	int addr = SWAP32(h->smcBootAddr);
	uint32_t s = SWAP32(h->smcBootSize);
	int size = s;
	uint32_t a;

'''
HS = '''void getImageSmc(void)
{
	struct flashhdr *h = (struct flashhdr *)xb.dump;
	int addr = SWAP32(h->smcBootAddr);
	int s = SWAP32(h->smcBootSize);
	int size;
	uint32_t a;

'''
AA = {'t6': Z + f'unsigned t = addr;\n if (t != 0x1000) {{ if (t != 0x800) {{ {L} }} }}\n',
      't6a': Z + f'a = addr;\n if (a != 0x1000) {{ if (a != 0x800) {{ {L} }} }}\n'}
B3 = f'if (addr == 0x800) {{ size = 0x3800; {S3800} }} else {{ size = 0x3000; {S3000} }} a = addr;'
B7 = f'a = addr; if (a == 0x800) {{ size = 0x3800; {S3800} }} else {{ size = 0x3000; {S3000} }}'
TS = {
    'n': lambda b: 'if (s != 0x3000) { if (s != 0x3800) {%s} else {a = addr;} } else {a = addr;}\n' % b,
    'nr': lambda b: 'if (s != 0x3800) { if (s != 0x3000) {%s} else {a = addr;} } else {a = addr;}\n' % b,
    'ng': lambda b: 'if (s != 0x3000) { if (s != 0x3800) {%s goto done; } } a = addr;\n done:\n' % b,
    'ngr': lambda b: 'if (s != 0x3800) { if (s != 0x3000) {%s goto done; } } a = addr;\n done:\n' % b,
}
TH = {
    'n': lambda b: 'if (s != 0x3000) { if (s != 0x3800) {%s} else {size = s; a = addr;} } else {size = s; a = addr;}\n' % b,
    'nr': lambda b: 'if (s != 0x3800) { if (s != 0x3000) {%s} else {size = s; a = addr;} } else {size = s; a = addr;}\n' % b,
    'ng': lambda b: 'if (s != 0x3000) { if (s != 0x3800) {%s goto done; } } size = s; a = addr;\n done:\n' % b,
    'ngr': lambda b: 'if (s != 0x3800) { if (s != 0x3000) {%s goto done; } } size = s; a = addr;\n done:\n' % b,
}
AX = []
for kh, h, T in (('hi', HI, TS), ('hr', HR, TS), ('hs', HS, TH)):
    for ka, aa in AA.items():
        for kt, f in T.items():
            for kb, b in (('k3', B3), ('k7', B7)):
                for kr, v in (('a', 'a'), ('u', 'addr')):
                    AX.append(('.'.join((kh, ka, kt, kb, kr)), [(OLD, h + aa + f(b) + rest(1, v))]))
AXES = [AX]
