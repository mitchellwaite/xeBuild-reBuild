"""getImageSmc: hint-free.  Two logs; the second test nested so that threading the zero arm's path raises P(bad) above 50%
(n3 in gen_ir113: 60.6% x 85.8% at the end, but unmerged); a second name for addr so ifcombine merges the nested tests."""
FOCUS = ['_getImageSmc']
BASE = 'tools/wip/dehint/drafts/image_read_attempt6.c'
import re
src = open(BASE, newline='').read().replace('\r\n', '\n')
i = src.index('__attribute__((optimize("no-if-conversion", "no-if-conversion2", "no-tree-tail-merge"))) void getImageSmc')
j = src.index('void getImageKv(void)')
OLD = src[i:j]
L = 'log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", addr);\n addr = 0x1000;\n'
Z = f'if (!addr) {{ {L} }}\n'
TA = {
    'cast': Z + f'if ((uint32_t)addr != 0x800) {{ if ((uint32_t)addr != 0x1000) {{ {L} }} }}\n',
    'a': Z + f'uint32_t a = addr;\n if (a != 0x800) {{ if (a != 0x1000) {{ {L} }} }}\n',
    'bare': Z + f'if (addr != 0x800) {{ if (addr != 0x1000) {{ {L} }} }}\n',
    'and': Z + f'if (addr != 0x800 && addr != 0x1000) {{ {L} }}\n',
    'cand': Z + f'if ((uint32_t)addr != 0x800 && (uint32_t)addr != 0x1000) {{ {L} }}\n',
    'sa': Z + f'short a = addr;\n if (addr != 0x800) {{ if (addr != 0x1000) {{ {L} }} }}\n',
}
S1 = '''if (addr == 0x800) {
			size = 0x3800;
			log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3800\\n", size);
		} else {
			size = 0x3000;
			log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3000\\n", size);
		}
'''
TS = {
    'and': 'if (size != 0x3000 && size != 0x3800) {' + S1 + '}\n',
    'cast': 'if ((uint32_t)size != 0x3000) { if ((uint32_t)size != 0x3800) {' + S1 + '} }\n',
    's': 'uint32_t s = size;\n if (s != 0x3000) { if (s != 0x3800) {' + S1 + '} }\n',
    'bare': 'if (size != 0x3000) { if (size != 0x3800) {' + S1 + '} }\n',
}
REST = OLD[OLD.index('if (__builtin_expect(addr < 528 * xb.dumpPages, 0)) {'):]
REST = REST[:REST.index('	return;\nbad:')] + '}\n\n'
EXK = {'ex': REST, 'e0': REST.replace('__builtin_expect(addr < 528 * xb.dumpPages, 0)', 'addr < 528 * xb.dumpPages')}
HEAD = '''void getImageSmc(void)
{
	struct flashhdr *h = (struct flashhdr *)xb.dump;
	int addr = SWAP32(h->smcBootAddr);
	int size = SWAP32(h->smcBootSize);

'''
AX = []
for ka, a in TA.items():
    for ks, s in TS.items():
        for ke, e in EXK.items():
            AX.append((ka + '.' + ks + '.' + ke, [(OLD, HEAD + a + s + e)]))
AXES = [AX]
