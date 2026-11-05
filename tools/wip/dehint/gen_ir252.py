"""Attempt 20: from src's getImageSmc: (1) E as a recheck flag rather than a sum; (2) fewer gotos around the size arms, at no cost in bytes."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ir17lib import put, score, base, A, B, L38, L30

SRC = base[A:B]
SRC = SRC[SRC.index('void getImageSmc(void)'):].rstrip() + '\n'
OLD_E = '''	{
		int excess = (size & ~0x800u) - 0x3000;

		addr += excess;
	}
'''
assert OLD_E in SRC
ES = {
    'v_mul': '{ int valid = (size & ~0x800u) == 0x3000; addr *= valid; }',
    'v_neg': '{ int valid = (size & ~0x800u) == 0x3000; addr &= -valid; }',
    'v_and': '{ unsigned base = size & ~0x800u; addr &= -(base == 0x3000); }',
    'v_tern': '{ unsigned base = size & ~0x800u; addr = base == 0x3000 ? addr : 0; }',
    'v_ifsz': '{ unsigned base = size & ~0x800u; if (base != 0x3000) addr = size; }',
    'v_ifb': '{ unsigned base = size & ~0x800u; if (base != 0x3000) addr = base; }',
    'pad': '{ unsigned base = size & ~0x800u; addr += base & 0xfff; }',
    'padi': '{ unsigned base = size & ~0x800u; int pad = base & 0xfff; addr += pad; }',
    'ali': '{ unsigned base = size & ~0x800u; addr &= ~(base & 0xfff); }',
    'alii': '{ unsigned base = size & ~0x800u; int m = base & 0xfff; addr &= ~m; }',
}
out = {k: SRC.replace(OLD_E, '\t' + v + '\n') for k, v in ES.items()}

ARM = '''	if (bad > 0) {
		o = addr != 0x800;
		if (o > 0)
			goto use3000;
		size = 0x3800;
		log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3800\\n", size);
		goto check;
	}
	goto sizeOk;
'''
assert ARM in SRC
L38T = '''		size = 0x3800;
		log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3800\\n", size);
'''
out['l_early'] = SRC.replace(ARM, '''	if (bad <= 0)
		goto sizeOk;
	o = addr != 0x800;
	if (o > 0)
		goto use3000;
''' + L38T + '''	goto check;
''')
out['l_noo'] = SRC.replace(ARM, '''	if (bad <= 0)
		goto sizeOk;
	if (addr != 0x800)
		goto use3000;
''' + L38T + '''	goto check;
''')
out['l_else'] = SRC.replace(ARM, ARM.replace('\t}\n\tgoto sizeOk;', '\t} else\n\t\tgoto sizeOk;'))
out['l_o38'] = SRC.replace(ARM, '''	if (bad > 0) {
		o = addr != 0x800;
		if (o <= 0) {
''' + L38T + '''			goto check;
		}
		goto use3000;
	}
	goto sizeOk;
''')
out['l_early38'] = SRC.replace(ARM, '''	if (bad <= 0)
		goto sizeOk;
	o = addr != 0x800;
	if (o <= 0) {
''' + L38T + '''		goto check;
	}
	goto use3000;
''')
# t's nest as one test; the bad log before the size test by flag
NEST = '''	if (t != 0x1000) {
		if (t != 0x800)
			goto badAddr;
	}
'''
assert NEST in SRC
out['l_tand'] = SRC.replace(NEST, '''	if (t != 0x1000 && t != 0x800)
		goto badAddr;
''')

if __name__ == '__main__':
    res = []
    for k, f in out.items():
        s = score(put(f))
        if s[0] == 'E':
            print(k, s[1][:300])
            continue
        res.append((s[1], s[0], k, s[2], s[3]))
    res.sort(key=lambda x: (x[0], x[1]))
    for r in res:
        print(r)
