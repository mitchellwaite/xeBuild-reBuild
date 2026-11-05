"""getImageSmc with no hint at all, after findAnchor's lesson (a flag, not a compound condition): forms of the address and size checks."""
FOCUS = ['_getImageSmc']
BASE = 'tools/wip/dehint/drafts/image_read_attempt6.c'
import os
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'drafts', 'image_read_attempt6.c'), newline='').read().replace('\r\n', '\n')
a = src.index('__attribute__((optimize("no-if-conversion", "no-if-conversion2", "no-tree-tail-merge"))) void getImageSmc')
b = src.index('	if (__builtin_expect(addr < 528 * xb.dumpPages, 0)) {')
OLD1 = src[a:b]
LB = 'log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", addr);\n addr = 0x1000;\n'
L38 = 'size = 0x3800;\n log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3800\\n", size);\n'
L30 = 'size = 0x3000;\n log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3000\\n", size);\n'
FIX = f'if (addr == 0x800) {{ {L38} }} else {{ {L30} }}\n'
ADDR = {
    'seq': f'if (!addr) {{ {LB} }}\n if (addr != 0x800 && addr != 0x1000) {{ {LB} }}\n',
    'eif': f'if (!addr) {{ {LB} }} else if (addr != 0x800 && addr != 0x1000) {{ {LB} }}\n',
    'nest': f'if (!addr) {{ {LB} }}\n if (addr != 0x800) {{ if (addr != 0x1000) {{ {LB} }} }}\n',
    'enest': f'if (!addr) {{ {LB} }} else if (addr != 0x800) {{ if (addr != 0x1000) {{ {LB} }} }}\n',
    'or': f'if (!addr) {{ {LB} }}\n if (addr == 0x800 || addr == 0x1000) ; else {{ {LB} }}\n',
    'ladder': f'if (!addr) {{ {LB} }} else if (addr == 0x800) ; else if (addr == 0x1000) ; else {{ {LB} }}\n',
    'flag': f'if (!addr) {{ {LB} }}\n ok = 0;\n if (addr == 0x800) ok = 1;\n if (addr == 0x1000) ok = 1;\n if (!ok) {{ {LB} }}\n',
    'flag2': f'if (!addr) {{ {LB} }}\n ok = addr == 0x800 || addr == 0x1000;\n if (!ok) {{ {LB} }}\n',
    'flag3': f'ok = 1;\n if (!addr) ok = 0;\n if (addr != 0x800 && addr != 0x1000) ok = 0;\n if (!ok) {{ {LB} }}\n',
    'flag4': f'ok = 0;\n if (addr) {{ if (addr == 0x800 || addr == 0x1000) ok = 1; }}\n if (!ok) {{ {LB} }}\n',
    'one': f'if (!addr || (addr != 0x800 && addr != 0x1000)) {{ {LB} }}\n',
    'onen': f'if (addr == 0x800 || addr == 0x1000) ; else {{ {LB} }}\n',
}
SIZE = {
    'and': f'if (size != 0x3000 && size != 0x3800) {{ {FIX} }}\n',
    'nest': f'if (size != 0x3000) {{ if (size != 0x3800) {{ {FIX} }} }}\n',
    'or': f'if (size == 0x3000 || size == 0x3800) ; else {{ {FIX} }}\n',
    'ladder': f'if (size == 0x3000) ; else if (size == 0x3800) ; else {{ {FIX} }}\n',
    'flag': f'ok2 = size == 0x3000 || size == 0x3800;\n if (!ok2) {{ {FIX} }}\n',
    'flag2': f'ok2 = 0;\n if (size == 0x3000) ok2 = 1;\n if (size == 0x3800) ok2 = 1;\n if (!ok2) {{ {FIX} }}\n',
    'addr': f'if (addr == 0x800) {{ if (size != 0x3000 && size != 0x3800) {{ {L38} }} }} else if (size != 0x3000 && size != 0x3800) {{ {L30} }}\n',
}
HEAD = '''void getImageSmc(void)
{
	struct flashhdr *h = (struct flashhdr *)xb.dump;
	%s addr = SWAP32(h->smcBootAddr);
	%s size = SWAP32(h->smcBootSize);
	int ok, ok2;

'''
TYPES = {'ii': ('int', 'int'), 'ui': ('uint32_t', 'int'), 'iu': ('int', 'uint32_t'), 'uu': ('uint32_t', 'uint32_t')}
AX = [(t + '.' + x + '.' + y, [(OLD1, HEAD % TYPES[t] + ADDR[x] + SIZE[y])]) for t in TYPES for x in ADDR for y in SIZE]
EX = 'if (__builtin_expect(addr < 528 * xb.dumpPages, 0)) {'
TAIL = '''	return;
bad:
	bhot: __attribute__((hot));
	log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", addr);
	addr = 0x1000;
	goto bback;
}
'''
AXES = [AX, [('', [(EX, 'if (addr < 528 * xb.dumpPages) {'), (TAIL, '}\n')])]]
