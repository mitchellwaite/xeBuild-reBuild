# attempt 17: gen_iw235's left, rounding and s[9] spellings, anchored on current src text, x tail x blk's place, on IWB (na.c or ifb.c), by full signature.
import os
BASE = os.environ.get('IWB', 'build/iw/a17/ifb.c')
OLD = '''						left = (off & 0x1ffff) ? 256 - (off & 0x1ffff) / 512 : 256;
						if (pages & 3)
							pages = (pages + 4) & ~3;
						s[9] = (left - (int)pages) >> 2;
'''
I = '\t' * 6
def f(s):
    return ''.join(I + l + '\n' for l in s.split('\n'))
L4 = 'if (off & 0x1ffff)\n	left = 256 - (off & 0x1ffff) / 512;\nelse\n	left = 256;\n'
L3 = 'left = (off & 0x1ffff) ? 256 - (off & 0x1ffff) / 512 : 256;\n'
L8 = 'left = 256;\nif (off & 0x1ffff)\n	left -= (off & 0x1ffff) / 512;\n'
R = 'if (pages & 3)\n	pages = (pages + 4) & ~3;\n'
R2 = 'if (pages & 3) {\n	pages += 4;\n	pages &= ~3;\n}\n'
ES = [('e1', 's[9] = (left - (int)pages) >> 2;'), ('e2', 'left -= (int)pages;\ns[9] = left >> 2;'), ('e3', 'left = left - pages;\ns[9] = left >> 2;'), ('e4', 's[9] = (int)(left - pages) >> 2;'), ('e5', 's[9] = (left - (int)pages) / 4;')]
CA = []
for ln, l in [('L4', L4), ('L3', L3), ('L8', L8)]:
    for rn, r in [('r', R), ('R', R2)]:
        for en, e in ES:
            CA.append((ln + rn + en, [(OLD, f(l + r + e))]))
TL = [('', []), ('tb', [('	setBeU16(off >> 14, (uint8_t *)&xb.fsBlock);\n', '	setBeU16(blk, (uint8_t *)&xb.fsBlock);\n')])]
DD = [('', []), ('nd', [('	if ((off & 0x3fff) > 0x3fff)\n		off += 0x4000;\n', '')])]
AXES = [CA, TL, DD]
FLAGS = []
