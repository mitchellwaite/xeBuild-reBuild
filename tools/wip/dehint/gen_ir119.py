"""getImageSmc: small forms around gen_ir118 t6.and.k3.ex (9 loose lines, only exp_smc kept)."""
FOCUS = ['_getImageSmc']
BASE = 'tools/wip/dehint/drafts/image_read_attempt6.c'
src = open(BASE, newline='').read().replace('\r\n', '\n')
i = src.index('__attribute__((optimize("no-if-conversion", "no-if-conversion2", "no-tree-tail-merge"))) void getImageSmc')
j = src.index('void getImageKv(void)')
OLD = src[i:j]
L = 'log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", addr);\n addr = 0x1000;\n'
LA = 'log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", addr);\n a = addr = 0x1000;\n'
Z = f'if (!addr) {{ {L} }}\n'
S3800 = 'log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3800\\n", size);\n'
S3000 = 'log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3000\\n", size);\n'
REST = OLD[OLD.index('if (__builtin_expect(addr < 528 * xb.dumpPages, 0)) {'):]
REST = REST[:REST.index('	return;\nbad:')] + '}\n\n'
def rest(v, form):
    r = REST.replace('xb.dump + addr', 'xb.dump + ' + v)
    return r.replace('__builtin_expect(addr < 528 * xb.dumpPages, 0)', form % v)
H = {
 'd1': '''void getImageSmc(void)
{
	struct flashhdr *h = (struct flashhdr *)xb.dump;
	int addr = SWAP32(h->smcBootAddr);
	int size = SWAP32(h->smcBootSize);
	uint32_t a;

''',
 'd2': '''void getImageSmc(void)
{
	struct flashhdr *h = (struct flashhdr *)xb.dump;
	uint32_t a;
	int addr = SWAP32(h->smcBootAddr);
	int size = SWAP32(h->smcBootSize);

''',
}
AD = {
    't6': Z + f'unsigned t = addr;\n if (t != 0x1000) {{ if (t != 0x800) {{ {L} }} }}\n',
    't6s': Z + f'{{ unsigned t = addr;\n if (t != 0x1000) {{ if (t != 0x800) {{ {L} }} }} }}\n',
    'ta': Z + f'a = addr;\n if (a != 0x1000) {{ if (a != 0x800) {{ {L} }} }}\n',
    'tc': Z + f'if ((unsigned)addr != 0x1000) {{ if ((unsigned)addr != 0x800) {{ {L} }} }}\n',
    'tb': Z + f'if (addr != 0x1000) {{ if (addr != 0x800) {{ {L} }} }}\n',
    'ta2': Z + f'a = addr;\n if (a != 0x1000) {{ if (a != 0x800) {{ {LA} }} }}\n',
}
def test(body, els):
    return 'if (size != 0x3000 && size != 0x3800) {%s} else {%s}\n' % (body, els) if els else 'if (size != 0x3000 && size != 0x3800) {%s}\n' % body
SZ = {
    'k3': test(f'if (addr == 0x800) {{ size = 0x3800; {S3800} }} else {{ size = 0x3000; {S3000} }} a = addr;', 'a = addr;'),
    'k1': 'a = addr;\n' + test(f'if (addr == 0x800) {{ size = 0x3800; {S3800} }} else {{ size = 0x3000; {S3000} }}', ''),
    'k5': test(f'if (addr == 0x800) {{ size = 0x3800; {S3800} }} else {{ size = 0x3000; {S3000} }}', '') + 'a = addr;\n',
    'k7': test(f'a = addr; if (a == 0x800) {{ size = 0x3800; {S3800} }} else {{ size = 0x3000; {S3000} }}', 'a = addr;'),
    'k8': test(f'if (addr == 0x800) {{ size = 0x3800; {S3800} }} else {{ size = 0x3000; {S3000} }} a = addr;', 'a = (uint32_t)addr;'),
    'k9': test(f'if (addr != 0x800) {{ size = 0x3000; {S3000} }} else {{ size = 0x3800; {S3800} }} a = addr;', 'a = addr;'),
}
RF = {'a': ('a', '__builtin_expect(%s < 528 * xb.dumpPages, 0)'), 'ad': ('addr', '__builtin_expect((uint32_t)%s < 528 * xb.dumpPages, 0)')}
AX = []
for kh, h in H.items():
    for ka, aa in AD.items():
        for ks, s in SZ.items():
            for kr, (v, f) in RF.items():
                AX.append(('.'.join((kh, ka, ks, kr)), [(OLD, h + aa + s + rest(v, f))]))
AXES = [AX]
