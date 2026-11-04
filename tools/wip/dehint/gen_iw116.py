# attempt 7: on r0 (IWB=): natural temporaries of the FS loop and the outer loop x optimize attribute, viewed with iw_tuples
import os
OPT = '__attribute__((optimize("no-tree-scev-cprop"))) void writeFsTable'
DECL = '	uint32_t b;\n	uint32_t i;\n'
FSH = '		for (i = 0; i < blocks; i++) {\n'
F1 = '				fsTable[start + i - xb.fsStart] = SWAP16_IMAGE_WRITE(next);\n'
F2 = '				fsTable[start + i - xb.fsStart] = SWAP16_IMAGE_WRITE(start + i - xb.fsStart + 1);\n'
NT = '			if (next != 0 && next != 0xffff) {\n'
BLKU = '				((struct spb *)s)->b2lo = BLK >> 8;\n'
OUT = '	for (b = 0; b < blocks; b++) {\n'
AXES = [
 [('', []), ('noopt', [(OPT, 'void writeFsTable')])],
 [('', []),
  ('e1', [(DECL, DECL + '	uint32_t e;\n'), (F1, '				fsTable[e] = SWAP16_IMAGE_WRITE(next);\n'),
          (F2, '				fsTable[e] = SWAP16_IMAGE_WRITE(e + 1);\n'), (NT, '			e = start + i - xb.fsStart;\n' + NT)]),
  ('e2', [(DECL, DECL + '	uint32_t e;\n'), (F2, '				e = start + i - xb.fsStart;\n				fsTable[e] = SWAP16_IMAGE_WRITE(e + 1);\n')]),
  ('e3', [(DECL, DECL + '	uint32_t e;\n'), (FSH, '		e = start - xb.fsStart;\n' + FSH),
          (F1, '				fsTable[e + i] = SWAP16_IMAGE_WRITE(next);\n'), (F2, '				fsTable[e + i] = SWAP16_IMAGE_WRITE(e + i + 1);\n')]),
 ],
 [('', []),
  ('n1', [(DECL, DECL + '	int chain;\n'), (FSH, '		chain = next != 0 && next != 0xffff;\n' + FSH), (NT, '			if (chain) {\n')]),
  ('n2', [(DECL, DECL + '	int chain;\n'), (NT, '			chain = next != 0 && next != 0xffff;\n			if (chain) {\n')]),
 ],
 [('', []),
  ('b1', [(DECL, DECL + '	uint32_t blk;\n'), (OUT, OUT + '		blk = start + b;\n'), (BLKU, '				((struct spb *)s)->b2lo = blk >> 8;\n')]),
  ('b2', [(DECL, DECL + '	uint32_t blk;\n'), (BLKU, '				blk = BLK;\n				((struct spb *)s)->b2lo = blk >> 8;\n				s[1] = blk;\n'), ('				s[1] = BLK;\n', '')]),
  ('b3', [(DECL, DECL + '	uint32_t blk;\n'), (BLKU, '				blk = BLK >> 8;\n				((struct spb *)s)->b2lo = blk;\n')]),
 ],
]
BASE = os.environ.get('IWB', 'build/iw/a6/r0.c')
FLAGS = []
