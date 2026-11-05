"""getImageSmc: the else of the size test assigns size from a raw unsigned value: a real statement in the ok join with no named a,
so PRE's conversion of addr stays anonymous (hinted: r98 = _20) and goes into that block."""
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
EX = {'ex': REST, 'e0': REST.replace('__builtin_expect(addr < 528 * xb.dumpPages, 0)', 'addr < 528 * xb.dumpPages')}
H = {
 'h1': '''void getImageSmc(void)
{
	struct flashhdr *h = (struct flashhdr *)xb.dump;
	int addr = SWAP32(h->smcBootAddr);
	uint32_t s = SWAP32(h->smcBootSize);
	int size;

''',
 'h2': '''void getImageSmc(void)
{
	struct flashhdr *h = (struct flashhdr *)xb.dump;
	int addr = SWAP32(h->smcBootAddr);
	int size;
	uint32_t s = SWAP32(h->smcBootSize);

''',
}
ADDR = {
    't6': Z + f'unsigned t = addr;\n if (t != 0x1000) {{ if (t != 0x800) {{ {L} }} }}\n',
    't7': Z + f'unsigned t = addr;\n if (t != 0x800) {{ if (t != 0x1000) {{ {L} }} }}\n',
    'and': Z + f'if (addr != 0x800 && addr != 0x1000) {{ {L} }}\n',
    'b6': Z + f'if (addr != 0x1000) {{ if (addr != 0x800) {{ {L} }} }}\n',
    'c6': Z + f'if ((unsigned)addr != 0x1000) {{ if ((unsigned)addr != 0x800) {{ {L} }} }}\n',
}
ARM = f'if (addr == 0x800) {{ size = 0x3800; {S3800} }} else {{ size = 0x3000; {S3000} }}'
TS = {
    'and': 'if (s != 0x3000 && s != 0x3800) {%s} else {size = s;}\n',
    'rand': 'if (s != 0x3800 && s != 0x3000) {%s} else {size = s;}\n',
    'nest': 'if (s != 0x3000) { if (s != 0x3800) {%s} else {size = s;} } else {size = s;}\n',
    'nestr': 'if (s != 0x3800) { if (s != 0x3000) {%s} else {size = s;} } else {size = s;}\n',
    'nestk': 'if (s != 0x3000) { if (s != 0x3800) {%s} else {size = 0x3800;} } else {size = 0x3000;}\n',
    'rev': 'if (s == 0x3000 || s == 0x3800) {size = s;} else {%s}\n',
    'first': 'size = s;\n if (s != 0x3000 && s != 0x3800) {%s}\n',
}
AX = []
for kh, hh in H.items():
    for ka, aa in ADDR.items():
        for kt, t in TS.items():
            for ke, e in EX.items():
                AX.append(('.'.join((kh, ka, kt, ke)), [(OLD, hh + aa + (t % ARM) + e)]))
AXES = [AX]
