"""getImageSmc: gen_ir118's t6 for addr, forms of the size test (P over 50: nested on a uint32_t copy, reversed order) with a real a."""
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
H = '''void getImageSmc(void)
{
	struct flashhdr *h = (struct flashhdr *)xb.dump;
	int addr = SWAP32(h->smcBootAddr);
	int size = SWAP32(h->smcBootSize);
	uint32_t a;

'''
AA = Z + f'unsigned t = addr;\n if (t != 0x1000) {{ if (t != 0x800) {{ {L} }} }}\n'
B3 = f'if (addr == 0x800) {{ size = 0x3800; {S3800} }} else {{ size = 0x3000; {S3000} }} a = addr;'
B7 = f'a = addr; if (a == 0x800) {{ size = 0x3800; {S3800} }} else {{ size = 0x3000; {S3000} }}'
TS = {
    'and': lambda b: 'if (size != 0x3000 && size != 0x3800) {%s} else {a = addr;}\n' % b,
    'rand': lambda b: 'if (size != 0x3800 && size != 0x3000) {%s} else {a = addr;}\n' % b,
    'un': lambda b: 'unsigned s = size;\n if (s != 0x3000) { if (s != 0x3800) {%s} else {a = addr;} } else {a = addr;}\n' % b,
    'run': lambda b: 'unsigned s = size;\n if (s != 0x3800) { if (s != 0x3000) {%s} else {a = addr;} } else {a = addr;}\n' % b,
    'rbare': lambda b: 'if (size != 0x3800) { if (size != 0x3000) {%s} else {a = addr;} } else {a = addr;}\n' % b,
    'run2': lambda b: 'unsigned s = size; a = addr;\n if (s != 0x3800) { if (s != 0x3000) {%s} }\n' % b.replace('a = addr;', ''),
    'and2': lambda b: 'a = addr;\n if (size != 0x3800 && size != 0x3000) {%s}\n' % b.replace('a = addr;', ''),
}
AX = []
for ks, f in TS.items():
    for kb, b in (('k3', B3), ('k7', B7)):
        for ex in (1, 0):
            AX.append(('.'.join((ks, kb, 'ex' if ex else 'e0')), [(OLD, H + AA + f(b) + rest(ex))]))
AXES = [AX]
