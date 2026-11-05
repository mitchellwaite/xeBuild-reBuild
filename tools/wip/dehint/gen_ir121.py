"""getImageSmc: gen_ir118's addr part (t6) with pin_addr kept in the size test's else, with and without a; milestone: attribute, 3 hot labels and the unreachable gone."""
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
H = '''void getImageSmc(void)
{
	struct flashhdr *h = (struct flashhdr *)xb.dump;
	int addr = SWAP32(h->smcBootAddr);
	int size = SWAP32(h->smcBootSize);

'''
AD = {
    't6': Z + f'unsigned t = addr;\n if (t != 0x1000) {{ if (t != 0x800) {{ {L} }} }}\n',
    't7': Z + f'unsigned t = addr;\n if (t != 0x800) {{ if (t != 0x1000) {{ {L} }} }}\n',
    'and': Z + f'if (addr != 0x800 && addr != 0x1000) {{ {L} }}\n',
}
BODY = f'if (addr == 0x800) {{ size = 0x3800; {S3800} }} else {{ size = 0x3000; {S3000} }}'
PINS = {'D': '__asm__("" : "+D"(addr));', 'r': '__asm__("" : "+r"(addr));', 'b': '__asm__("" : : "r"(addr));'}
ex = {'ex': lambda r: r, 'e0': lambda r: r.replace('__builtin_expect(addr < 528 * xb.dumpPages, 0)', 'addr < 528 * xb.dumpPages')}
AX = []
for ka, aa in AD.items():
    for kp, p in PINS.items():
        for ke, fe in ex.items():
            AX.append(('.'.join((ka, kp, ke)), [(OLD, H + aa + 'if (size != 0x3000 && size != 0x3800) {' + BODY + '} else {' + p + '}\n' + fe(REST))]))
AXES = [AX]
