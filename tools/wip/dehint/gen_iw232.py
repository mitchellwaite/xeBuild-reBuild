# attempt 16: the state's single dead test: position x condition x body (gen_iw222's lists), on the base in IWB, scored by full signature. Candidates must keep one dead test (5 tricks at most).
import os
BASE = os.environ.get('IWB', 'build/iw/a16/c4d.c')
DEAD = '	if ((off & 0x3fff) > 0x3fff)\n		off += 0x4000;\n'
POS = ['	buf = malloc(0x4000);\n', '	log_printf(1, "offset 0x%x len 0x4000', '	if (!xb.bigBlock)\n		goto small;\n']
CONDS = ['(off & 0x3fff) > 0x3fff', '(blk & 0xff) > 0xff', '(off >> 14) > 0x3ffff', '(off & 1) > 1', '(off >> 30) > 3', '(off & 0x1ffff) > 0x1ffff', '(blk >> 18) > 0x3fff']
BODIES = ['off += 0x4000;', 'off += 0x20000;', 'off++;', 'off = (off + 0x4000) & ~0x3fff;', 'off = (off + 0x3fff) & ~0x3fff;', 'off = (off + 0x20000) & ~0x1ffff;',
          'off = (off >> 14) << 14;', 'off = (blk + 1) << 14;', 'off = (off >> 14) * 0x4000 + 0x4000;', 'blk++;', 'blk = off >> 14;', 'blk = (off + 0x4000) >> 14;',
          'off += 0x4000; blk = off >> 14;', 'off = (off + 0x20000) & ~0x1ffff; blk = off >> 14;', 'return;', 'off = 0;', 'i++;', 'off -= off & 0x3fff;']
A = []
for pi, ps in enumerate(POS):
    for ci, c in enumerate(CONDS):
        for bi, b in enumerate(BODIES):
            A.append(('p%dc%db%d' % (pi, ci, bi), [(DEAD, ''), (ps, '	if (%s) {\n		%s\n	}\n' % (c, b) + ps)]))
AXES = [A]
FLAGS = []
