# attempt 5: natural imgAddFile on m1: forms that only touch imgAddFile (or imgFits), to flip `npages > p` in its inlined big copy
import os
import gen_iw69 as G69
BASE = os.environ.get('IWB', 'build/iw/a5/m1.c')
FITS = 'int imgFits(uint32_t off, uint32_t len)\n{\n	' + G69.FORMS['if1'] + '}\n'
BL = '		fsFiles[nFsFiles].block = SWAP16_IMAGE_WRITE((uint16_t)(off >> 14) - xb.fsStart);\n'
CALL = '''		if (!xb.bigBlock)
			imgAdd(off, data, len, 0, 0xffff, 1);
		else
			imgAdd(off, data, len, 0x2a, 0xffff, 1);
'''
OFFD = '	uint32_t off = imgSizeAligned();\n	uint32_t start, b, p, pages, npages, first, rem, tail, blocks;\n	uint16_t blk;\n	uint8_t *s;\n'
AXES = [
 [(k, [(FITS, 'int imgFits(uint32_t off, uint32_t len)\n{\n	' + G69.FORMS[k] + '}\n')] if k != 'if1' else []) for k in ('if1', 'else1', 'r0', 'lim1')],
 [('', []),
  ('b1', [(BL, '		blk = (off >> 14) - xb.fsStart;\n		fsFiles[nFsFiles].block = SWAP16_IMAGE_WRITE(blk);\n')]),
  ('b2', [(BL, '		blk = off >> 14;\n		fsFiles[nFsFiles].block = SWAP16_IMAGE_WRITE(blk - xb.fsStart);\n')]),
  ('b3', [(BL, '		fsFiles[nFsFiles].block = SWAP16_IMAGE_WRITE((off >> 14) - xb.fsStart);\n')]),
  ('b4', [(BL, '		fsFiles[nFsFiles].block = SWAP16_IMAGE_WRITE((uint16_t)((off >> 14) - xb.fsStart));\n')]),
 ],
 [('', []),
  ('c1', [(CALL, '		if (xb.bigBlock)\n			imgAdd(off, data, len, 0x2a, 0xffff, 1);\n		else\n			imgAdd(off, data, len, 0, 0xffff, 1);\n')]),
  ('c2', [(CALL, '		imgAdd(off, data, len, xb.bigBlock ? 0x2a : 0, 0xffff, 1);\n')]),
  ('c3', [(CALL, '		imgAdd(off, data, len, !xb.bigBlock ? 0 : 0x2a, 0xffff, 1);\n')]),
 ],
 [('', []),
  ('d1', [(OFFD, '	uint32_t off = imgSizeAligned();\n')]),
 ],
 [('', []),
  ('e1', [('		nFsFiles++;\n	} else {\n		log_printf(0, "\\n******* ERROR: adding %s', '		nFsFiles = nFsFiles + 1;\n	} else {\n		log_printf(0, "\\n******* ERROR: adding %s')]),
  ('e2', [('	if (imgFits(off, len)) {\n		fsFiles', '	int ok = imgFits(off, len);\n\n	if (ok) {\n		fsFiles')]),
 ],
]
FLAGS = []
