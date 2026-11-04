# attempt 17: one change at a time on drafts/image_write_a17.c, for the notes: what each shape in the draft is worth. `iw16sweep.py tools/wip/dehint/gen_iw250.py -n 30`.
import os
BASE = os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_a17.c')
PIN = '			/* no code: the slot order of t and partial (dead in every clone) */\n			__asm__("" :: "g"(t));\n'
AT = '__attribute__((optimize("no-tree-scev-cprop"))) void writeFsTable'
BLK = '			blk = start + b;\n			memset(s, 0, 16);\n'
BO = '						bo = off & 0x1ffff;\n'
LF = '						left = bo ? 256 - bo / 512 : 256;\n'
A = [('base', []),
 ('nopin', [(PIN, '')]),
 ('noattr', [(AT, 'void writeFsTable')]),
 ('malloc', [('xmalloc(xb.rawSize)', 'malloc(xb.rawSize)')]),
 ('blkperblock', [(BLK, '			memset(s, 0, 16);\n'), ('	for (b = 0; b < blocks; b++) {\n		small =', '	for (b = 0; b < blocks; b++) {\n		blk = start + b;\n		small =')]),
 ('nobo', [('			uint32_t bo;\n\n', ''), (BO, ''), (LF, '						left = (off & 0x1ffff) ? 256 - (off & 0x1ffff) / 512 : 256;\n')]),
 ('tearly', [("		p = 0;\n		t = type - '1';\n", '		p = 0;\n'), ('		small = type != 0', "		t = type - '1';\n		small = type != 0")]),
 ('int', [('s[9] = (left - pages) >> 2;', 's[9] = (left - (int)pages) >> 2;')]),
 ('tailoff', [('	setBeU16(blk, (uint8_t *)&xb.fsBlock);\n', '	setBeU16(off >> 14, (uint8_t *)&xb.fsBlock);\n')]),
 ('nolen', [('	len = i * 0x400;\n', ''), ('off, off + len);', 'off, off + 0x4000);'), ('buf, len, 0x2c', 'buf, i * 0x400, 0x2c'), ('buf, len, 0x30', 'buf, i * 0x400, 0x30'), ('	uint32_t len;\n', '')]),
 ('len4000', [('	len = i * 0x400;\n', '	len = 0x4000;\n')]),
 ('partial', [('if (partial > 0) {', 'if (partial) {')]),
 ('ifelse', [('	if (!xb.bigBlock)\n		goto small;\n	imgAdd(off, buf, len, 0x2c, 0x1ffe, 0);\n	goto done;\nsmall:\n	imgAdd(off, buf, len, 0x30, 0x1ffd, 0);\ndone:\n', '	if (xb.bigBlock)\n		imgAdd(off, buf, len, 0x2c, 0x1ffe, 0);\n	else\n		imgAdd(off, buf, len, 0x30, 0x1ffd, 0);\n')]),
 ('pagesq', [('						pages = len / 512;\n						if (len % 512)\n							pages++;\n						bo', '						pages = len % 512 ? len / 512 + 1 : len / 512;\n						bo')]),
]
AXES = [A]
FLAGS = []
