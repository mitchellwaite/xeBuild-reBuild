# attempt 15: a14 with one dead test (5 tricks if it lands: lnp2 gone, dead test stays). Wider than gen_iw206: bodies with up to 3 names, tail spelling, position.
# Reading from gen_iw220/221: the compare depends on the count of names freed above ccp2's layer and on the number of the last one.
import os
BASE = os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_a14.c')
POS = ['	buf = malloc(0x4000);\n', '	log_printf(1, "offset 0x%x len 0x4000', '	if (!xb.bigBlock)\n		goto small;\n']
CONDS = ['(off & 0x3fff) > 0x3fff', '(blk & 0xff) > 0xff', '(off >> 14) > 0x3ffff', '(off & 1) > 1', '(off >> 30) > 3', '(off & 0x1ffff) > 0x1ffff', '(blk >> 18) > 0x3fff']
BODIES = ['off += 0x4000;', 'off += 0x20000;', 'off++;', 'off = (off + 0x4000) & ~0x3fff;', 'off = (off + 0x3fff) & ~0x3fff;', 'off = (off + 0x20000) & ~0x1ffff;',
          'off = (off >> 14) << 14;', 'off = (blk + 1) << 14;', 'off = (off >> 14) * 0x4000 + 0x4000;', 'blk++;', 'blk = off >> 14;', 'blk = (off + 0x4000) >> 14;',
          'off += 0x4000; blk = off >> 14;', 'off = (off + 0x20000) & ~0x1ffff; blk = off >> 14;', 'return;', 'off = 0;', 'i++;', 'off -= off & 0x3fff;']
A = []
for pi, ps in enumerate(POS):
    for ci, c in enumerate(CONDS):
        for bi, b in enumerate(BODIES):
            A.append(('p%dc%db%d' % (pi, ci, bi), [(ps, '	if (%s) {\n		%s\n	}\n' % (c, b) + ps)]))
T = [('', []), ('tb', [('	setBeU16(off >> 14, (uint8_t *)&xb.fsBlock);\n', '	setBeU16(blk, (uint8_t *)&xb.fsBlock);\n')])]
AXES = [T, A]
FLAGS = []
