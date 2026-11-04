# attempt 17: full cross around n8 (drafts/image_write_a17.c): left's type x both pages x s[9] x tail x blk x call form x dead test x attribute, dropping dead + attribute together (no reduction).
import os
BASE = os.environ.get('IWB', 'build/iw/a17/n8.c')
D = '	uint32_t x, first, rem, tail, blocks, start, p, end, npages, pages, left;\n'
BG = '						pages = len % 512 ? len / 512 + 1 : len / 512;\n						left ='
SA = '				pages = len % 512 ? len / 512 + 1 : len / 512;\n				((struct sps'
S9 = 's[9] = (int)(left - pages) >> 2;'
BLK0 = '			blk = start + b;\n			memset(s, 0, 16);\n'
CALL = '	if (!xb.bigBlock)\n		goto small;\n	imgAdd(off, buf, i * 0x400, 0x2c, 0x1ffe, 0);\n	goto done;\nsmall:\n	imgAdd(off, buf, i * 0x400, 0x30, 0x1ffd, 0);\ndone:\n'
LOG = '	log_printf(1, "offset 0x%x len 0x4000 (end 0x%x)...", off, off + 0x4000);\n'
AXES = [
 [('', []), ('li', [(D, '	uint32_t x, first, rem, tail, blocks, start, p, end, npages, pages;\n	int left;\n')])],
 [('', []), ('bi', [(BG, '						pages = len / 512;\n						if (len % 512)\n							pages++;\n						left =')])],
 [('', []), ('si', [(SA, '				pages = len / 512;\n				if (len % 512)\n					pages++;\n				((struct sps')])],
 [('', []), ('e3', [(S9, 'left = left - pages;\n						s[9] = left >> 2;')]), ('e1', [(S9, 's[9] = (left - (int)pages) >> 2;')]), ('e0', [(S9, 's[9] = (left - pages) >> 2;')])],
 [('', []), ('tb', [('	setBeU16(off >> 14, (uint8_t *)&xb.fsBlock);\n', '	setBeU16(blk, (uint8_t *)&xb.fsBlock);\n')])],
 [('', []), ('ifb', [(CALL, '	if (xb.bigBlock)\n		imgAdd(off, buf, i * 0x400, 0x2c, 0x1ffe, 0);\n	else\n		imgAdd(off, buf, i * 0x400, 0x30, 0x1ffd, 0);\n')])],
 [('', []), ('dd', [(LOG, LOG + '	if ((off & 0x3fff) > 0x3fff)\n		off += 0x4000;\n')]), ('at', [('void writeFsTable(uint32_t off)\n{', '__attribute__((optimize("no-tree-scev-cprop"))) void writeFsTable(uint32_t off)\n{')])],
]
FLAGS = []
