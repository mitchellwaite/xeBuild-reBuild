# attempt 13: near13's (w2) block-number spellings per use, blk's position, and the small arm's pages statement. Names only.
import os
BASE = os.environ.get('IWB', 'build/iw/a13/w2.c')
B1 = '				((struct spb *)s)->b2lo = blk >> 8;\n'
B2 = '				s[1] = BLK;\n'
S1 = '				((struct sps *)s)->b1lo = BLK >> 8;\n'
S2 = '				s[0] = BLK;\n'
BL = '		blk = start + b;\n		partial ='
PQ = '				pages = len % 512 ? len / 512 + 1 : len / 512;\n'
AXES = [
 [('', []), ('a', [(B1, B1.replace('blk', 'BLK'))])],
 [('', []), ('b', [(B2, B2.replace('BLK', 'blk'))])],
 [('', []), ('c', [(S1, S1.replace('BLK', 'blk'))])],
 [('', []), ('d', [(S2, S2.replace('BLK', 'blk'))])],
 [('', []),
  ('e', [(BL, '		partial ='), ('		p = 0;\n		if (t < 15) {', '		blk = start + b;\n		p = 0;\n		if (t < 15) {')]),
  ('f', [(BL, '		partial ='), ('		for (end = p + npages;', '		blk = start + b;\n		for (end = p + npages;')]),
  ('g', [(BL, '		partial ='), ('			memset(s, 0, 16);\n			if (xb.bigBlock) {', '			blk = start + b;\n			memset(s, 0, 16);\n			if (xb.bigBlock) {')]),
 ],
 [('', []),
  ('h', [(PQ, '				pages = len / 512;\n				if (len % 512)\n					pages++;\n')]),
  ('i', [(PQ, '				if (len % 512)\n					pages = len / 512 + 1;\n				else\n					pages = len / 512;\n')]),
 ],
]
FLAGS = []
