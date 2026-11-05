"""getImageSmc: t6 and a real a (gen_ir118) with pin_addr kept in the size test's else: is E's conversion the only thing left?"""
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
H = '''void getImageSmc(void)
{
	struct flashhdr *h = (struct flashhdr *)xb.dump;
	int addr = SWAP32(h->smcBootAddr);
	int size = SWAP32(h->smcBootSize);
	uint32_t a;

'''
ADDR = {'t6': Z + f'unsigned t = addr;\n if (t != 0x1000) {{ if (t != 0x800) {{ {L} }} }}\n',
        'and': Z + f'if (addr != 0x800 && addr != 0x1000) {{ {L} }}\n'}
ARM = f'if (addr == 0x800) {{ size = 0x3800; {S3800} }} else {{ size = 0x3000; {S3000} }}'
ARMA = f'a = addr; if (a == 0x800) {{ size = 0x3800; {S3800} }} else {{ size = 0x3000; {S3000} }}'
T = 'if (size != 0x3000 && size != 0x3800) {%s} else {%s}\n'
PIN = {'D': '__asm__("" : "+D"(addr));', 'r': '__asm__("" : "+r"(addr));', 'i': '__asm__("" : : "D"(addr));', 'a': '__asm__("" : "+r"(a));', 'aD': '__asm__("" : "+b"(a));'}
AX = []
for ka, aa in ADDR.items():
    for kp, p in PIN.items():
        for kb, b, e in (('k3', ARM + ' a = addr;', p + ' a = addr;'), ('k3b', ARM + ' a = addr;', 'a = addr; ' + p), ('k7', ARMA, p + ' a = addr;'), ('k7b', ARMA, 'a = addr; ' + p)):
            for ex in (1, 0):
                AX.append(('.'.join((ka, kp, kb, 'ex' if ex else 'e0')), [(OLD, H + aa + (T % (b, e)) + rest(ex, 'a'))]))
AXES = [AX]
