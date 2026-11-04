# attempt 11: on build/iw/a10/l1.c (no hot label, clones right).  imgAddFile's one compare in the inlined big copy (`npages_134 > p_145`, reference `p_46 < npages_127`) with forms local to imgAddFile, no dead test.
import os
BASE = os.environ.get('IWB', 'build/iw/a10/l1.c')
BL = '		fsFiles[nFsFiles].block = SWAP16_IMAGE_WRITE((uint16_t)(off >> 14) - xb.fsStart);\n'
SZ = '		fsFiles[nFsFiles].size = SWAP32_IMAGE_WRITE(len);\n'
CP = '		strcpy(fsFiles[nFsFiles].name, name);\n'
TM = '		fsFiles[nFsFiles].time = *time;\n'
CALL = '''		if (!xb.bigBlock)
			imgAdd(off, data, len, 0, 0xffff, 1);
		else
			imgAdd(off, data, len, 0x2a, 0xffff, 1);
'''
INC = '		nFsFiles++;\n	} else {\n		log_printf(0, "\\n******* ERROR: adding %s'
HEAD = '	uint32_t off = imgSizeAligned();\n\n	if (imgFits(off, len)) {\n		fsFiles'
AXES = [
 [('', []),
  ('b1', [(BL, '		blk = (off >> 14) - xb.fsStart;\n		fsFiles[nFsFiles].block = SWAP16_IMAGE_WRITE(blk);\n'), (HEAD, HEAD.replace('off = imgSizeAligned();\n', 'off = imgSizeAligned();\n	uint16_t blk;\n'))]),
  ('b2', [(BL, '		blk = off >> 14;\n		fsFiles[nFsFiles].block = SWAP16_IMAGE_WRITE(blk - xb.fsStart);\n'), (HEAD, HEAD.replace('off = imgSizeAligned();\n', 'off = imgSizeAligned();\n	uint16_t blk;\n'))]),
  ('b3', [(BL, '		fsFiles[nFsFiles].block = SWAP16_IMAGE_WRITE((off >> 14) - xb.fsStart);\n')]),
  ('b4', [(BL, '		fsFiles[nFsFiles].block = SWAP16_IMAGE_WRITE((uint16_t)((off >> 14) - xb.fsStart));\n')]),
 ],
 [('', []),
  ('c1', [(CALL, '		if (xb.bigBlock)\n			imgAdd(off, data, len, 0x2a, 0xffff, 1);\n		else\n			imgAdd(off, data, len, 0, 0xffff, 1);\n')]),
  ('c2', [(CALL, '		imgAdd(off, data, len, xb.bigBlock ? 0x2a : 0, 0xffff, 1);\n')]),
  ('c3', [(CALL, '		imgAdd(off, data, len, !xb.bigBlock ? 0 : 0x2a, 0xffff, 1);\n')]),
  ('c4', [(CALL, '		uint8_t ty = 0;\n\n		if (xb.bigBlock)\n			ty = 0x2a;\n		imgAdd(off, data, len, ty, 0xffff, 1);\n')]),
 ],
 [('', []),
  ('e1', [(INC, INC.replace('nFsFiles++', 'nFsFiles = nFsFiles + 1'))]),
  ('e2', [(HEAD, '	uint32_t off = imgSizeAligned();\n	int ok = imgFits(off, len);\n\n	if (ok) {\n		fsFiles')]),
  ('e3', [(HEAD, '	uint32_t off = imgSizeAligned();\n\n	if (!imgFits(off, len)) {\n		log_printf(0, "\\n******* ERROR: adding %s will exceed available flash space! Skipped!\\n\\n", name);\n		return;\n	}\n	{\n		fsFiles'),
          ('		nFsFiles++;\n	} else {\n		log_printf(0, "\\n******* ERROR: adding %s will exceed available flash space! Skipped!\\n\\n", name);\n	}\n', '		nFsFiles++;\n	}\n')]),
  ('e4', [(HEAD, HEAD.replace('off = imgSizeAligned();\n', 'off = imgSizeAligned();\n	struct fsfile_ *f_unused_guard;\n').replace('	struct fsfile_ *f_unused_guard;\n', '	int n = nFsFiles;\n')),
          (BL, BL.replace('nFsFiles', 'n')), (SZ, SZ.replace('nFsFiles', 'n')), (CP, CP.replace('nFsFiles', 'n')), (TM, TM.replace('nFsFiles', 'n'))]),
 ],
 [('', []),
  ('o1', [(BL + SZ, SZ + BL)]),
  ('o2', [(CP + TM, TM + CP)]),
  ('o3', [(TM + CALL, CALL + TM)]),
 ],
]
FLAGS = []
FOCUS = ['_imgAddFile']
