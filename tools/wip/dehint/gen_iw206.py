# attempt 13: one dead test kept in writeFsTable on near13 (w2, one compare left): position x condition x body. Net -1 still if it fixes the compare (lnp2 gone, dead test stays).
import os
BASE = os.environ.get('IWB', 'build/iw/a13/w2.c')
ATTR = '__attribute__((optimize("no-tree-scev-cprop"))) void writeFsTable'
POS = ['	buf = malloc(0x4000);\n', '	for (i = 0; i < 16; i++) {\n		memcpy(p, (uint8_t *)fsTable', '	log_printf(1, "offset 0x%x len 0x4000', '	if (!xb.bigBlock)\n		goto small;\n',
       '	setBeU16(off >> 14, (uint8_t *)&xb.fsBlock);\n', '	fsTable[-xb.fsStart + blk]', '	free(buf);\n	}XX', '	setBeU16(0, (uint8_t *)&xb.fsReserved);\n']
CONDS = ['(off & 0x3fff) > 0x3fff', '(blk & 0xff) > 0xff', '(off >> 14) > 0x3ffff', 'i > 16', '(blk >> 18) > 0x3fff']
BODIES = ['blk++;', 'off++;', 'i++;', 'off += 0x4000;', 'blk += 2;']
A = [('', [])]
for pi, ps in enumerate(POS):
    if 'XX' in ps:
        continue
    for ci, c in enumerate(CONDS):
        if c == 'i > 16' and pi < 2:
            continue
        for bi, b in enumerate(BODIES):
            A.append(('p%dc%db%d' % (pi, ci, bi), [(ps, '	if (%s)\n		%s\n' % (c, b) + ps)]))
AXES = [[('', []), ('noattr', [(ATTR, 'void writeFsTable')])], A]
FLAGS = []
