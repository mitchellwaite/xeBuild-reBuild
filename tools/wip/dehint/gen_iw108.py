# attempt 6: r2 (r0 with `blk` declared) x original fsend: which LBA stores use a block-number local, where it's set, partial's two families
import os
OUT = '	for (b = 0; b < blocks; b++) {\n'
U1 = '				((struct spb *)s)->b2lo = BLK >> 8;\n'
U2 = '				s[1] = BLK;\n'
U3 = '				((struct sps *)s)->b1lo = BLK >> 8;\n'
U4 = '				s[0] = BLK;\n'
INNER = '		for (end = p + npages; p < end; p++) {\n'
FE = '			fsTable[start - xb.fsStart + blocks - 1] = SWAP16_IMAGE_WRITE(0x1fff);\n'
PART = "		partial = (len < 0x4000) & (type != 0) & (type != '0');\n"
M = '			memset(s, 0, 16);\n			if (xb.bigBlock) {\n				((struct spb'
AXES = [
 [('', []), ('u1', [(U1, U1.replace('BLK', 'blk'))])],
 [('', []), ('u2', [(U2, U2.replace('BLK', 'blk'))])],
 [('', []), ('u3', [(U3, U3.replace('BLK', 'blk'))])],
 [('', []), ('u4', [(U4, U4.replace('BLK', 'blk'))])],
 [('lo', [(OUT, OUT + '		blk = start + b;\n')]),
  ('li', [(INNER, INNER + '			blk = start + b;\n')]),
  ('lm', [(M, '			memset(s, 0, 16);\n			blk = start + b;\n			if (xb.bigBlock) {\n				((struct spb')]),
  ('lb', [(INNER, '		blk = start + b;\n' + INNER)]),
 ],
 [('', []), ('fo', [(FE, '			fsTable[start + blocks - 1 - xb.fsStart] = SWAP16_IMAGE_WRITE(0x1fff);\n')])],
 [('', []), ('f0', [(PART, "		partial = (type != 0) & (type != '0') && len < 0x4000;\n")])],
]
BASE = os.environ.get('IWB', 'build/iw/a6/r2.c')
FLAGS = []
