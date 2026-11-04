# attempt 16: the signed s[9] form `(left - (int)pages) >> 2` (imgAdd clean on c4, writeFsTable back to one compare) x left's spellings x blk positions x pages x tail, a15_dead base.
import os, importlib.util
here = os.path.dirname(os.path.abspath(__file__))
def L(n):
    sp = importlib.util.spec_from_file_location(n, os.path.join(here, n + '.py')); g = importlib.util.module_from_spec(sp); sp.loader.exec_module(g); return g
g7, g1, g8 = L('gen_iw207'), L('gen_iw231'), L('gen_iw228')
BASE = os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_a15_dead.c')
OLD = g1.OLD
I = '\t' * 6
def f(s):
    return ''.join(I + l + '\n' for l in s.split('\n'))
L4 = 'if (off & 0x1ffff)\n	left = 256 - (off & 0x1ffff) / 512;\nelse\n	left = 256;\n'
L3 = 'left = (off & 0x1ffff) ? 256 - (off & 0x1ffff) / 512 : 256;\n'
L8 = 'left = 256;\nif (off & 0x1ffff)\n	left -= (off & 0x1ffff) / 512;\n'
R = 'if (pages & 3)\n	pages = (pages + 4) & ~3;\n'
R2 = 'if (pages & 3) {\n	pages += 4;\n	pages &= ~3;\n}\n'
E1 = 's[9] = (left - (int)pages) >> 2;'
E2 = 'left -= (int)pages;\ns[9] = left >> 2;'
E3 = 'left = left - pages;\ns[9] = left >> 2;'
E4 = 's[9] = (int)(left - pages) >> 2;'
E5 = 's[9] = (left - (int)pages) / 4;'
CA = []
for ln, l in [('L4', L4), ('L3', L3), ('L8', L8)]:
    for rn, r in [('r', R), ('R', R2)]:
        for en, e in [('e1', E1), ('e2', E2), ('e3', E3), ('e4', E4), ('e5', E5)]:
            CA.append((ln + rn + en, [(OLD, f(l + r + e))]))
AB = [a for a in g8.AB if a[0] in ('ba', 'bm')]
AS = [a for a in g8.AS if a[0] in ('st', 'si')]
TL = [('', []), ('to', [('	setBeU16(blk, (uint8_t *)&xb.fsBlock);\n', '	setBeU16(off >> 14, (uint8_t *)&xb.fsBlock);\n')])]
A7 = g7.AXES
AXES = [CA, AB[:1], AS[:1], A7[0], A7[2], A7[4], TL]
FLAGS = []
