# attempt 7: on r0 (IWB=): a dead test inside writeFsTable only (imgAdd and its clones stay as they are): position x condition x body
import os
OPT = '__attribute__((optimize("no-tree-scev-cprop"))) void writeFsTable'
POS = {
 'P0': '	buf = malloc(0x4000);\n',
 'P1': '	p = buf;\n	for (i = 0; i < 16; i++) {\n		memcpy(p, (uint8_t *)fsTable',
 'P2': '	log_printf(1, "offset 0x%x len 0x4000 (end 0x%x)...", off, off + 0x4000);\n',
 'P3': '	if (!xb.bigBlock)\n		goto small;\n',
 'P4': '	setBeU16(blk, (uint8_t *)&xb.fsBlock);\n',
}
CONDS = {
 'co': '(off & 0x3fff) > 0x3fff',
 'cb': '(blk & 0xff) > 0xff',
 'cs': '(off >> 14) > 0x3ffff',
 'ci': 'i > 16',
}
BODIES = {'bb': 'blk++;', 'bo': 'off++;', 'bi': 'i++;', 'bf': 'off += 0x4000;'}
A = [('', [])]
for pn, ps in POS.items():
    for cn, c in CONDS.items():
        if cn == 'ci' and pn in ('P0', 'P1'):
            continue
        for bn, b in BODIES.items():
            if pn == 'P4' and bn in ('bo', 'bf', 'bi'):
                continue
            A.append((pn + cn + bn, [(ps, '	if (%s)\n		%s\n%s' % (c, b, ps))]))
AXES = [
 [('', []), ('noopt', [(OPT, 'void writeFsTable')])],
 A,
]
BASE = os.environ.get('IWB', 'build/iw/a6/r0.c')
FLAGS = []
