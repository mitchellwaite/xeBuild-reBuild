# attempt 17: the if/else call form (Linux's; IWB = src minus optimize with it) x length x tail x dead test x attribute x blk's place x (int). Also the source of ifb's C1 reading: `<<<<<<<>`.
import os
BASE = os.environ.get('IWB', 'build/iw/a17/ifb.c')
DEAD = '	if ((off & 0x3fff) > 0x3fff)\n		off += 0x4000;\n'
A = '	imgAdd(off, buf, i * 0x400, 0x2c, 0x1ffe, 0);\n	else\n		imgAdd(off, buf, i * 0x400, 0x30, 0x1ffd, 0);\n'
def L(n):
    return A.replace('i * 0x400', n)
BLK0 = '			blk = start + b;\n			memset(s, 0, 16);\n'
AXES = [
 [('', []), ('l4', [(A, L('0x4000'))]), ('lp', [(A, L('p - buf'))])],
 [('', []), ('tb', [('	setBeU16(off >> 14, (uint8_t *)&xb.fsBlock);\n', '	setBeU16(blk, (uint8_t *)&xb.fsBlock);\n')])],
 [('', []), ('nd', [(DEAD, '')])],
 [('', []), ('at', [('void writeFsTable(uint32_t off)\n{', '__attribute__((optimize("no-tree-scev-cprop"))) void writeFsTable(uint32_t off)\n{')])],
 [('', []), ('bk', [(BLK0, '			memset(s, 0, 16);\n'), ('	for (b = 0; b < blocks; b++) {\n		small =', '	for (b = 0; b < blocks; b++) {\n		blk = start + b;\n		small =')])],
 [('', []), ('ni', [('s[9] = (left - (int)pages) >> 2;', 's[9] = (left - pages) >> 2;')])],
]
FLAGS = []
