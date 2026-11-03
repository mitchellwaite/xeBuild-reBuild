# attempt 6: r0 with a block-number variable used in some of the LBA stores (gen_iw104 `bv` makes writeFsTable match but loses `b`'s iv in constprop.4)
import os
OUT = '	for (b = 0; b < blocks; b++) {\n'
U1 = '				((struct spb *)s)->b2lo = BLK >> 8;\n'
U2 = '				s[1] = BLK;\n'
U3 = '				((struct sps *)s)->b1lo = BLK >> 8;\n'
U4 = '				s[0] = BLK;\n'
INNER = '		for (end = p + npages; p < end; p++) {\n'
SS = '			s = xb.spare + (pg + p + b * 32) * 16;\n'
AXES = [
 [('', []), ('u1', [(U1, U1.replace('BLK', 'blk'))])],
 [('', []), ('u2', [(U2, U2.replace('BLK', 'blk'))])],
 [('', []), ('u3', [(U3, U3.replace('BLK', 'blk'))])],
 [('', []), ('u4', [(U4, U4.replace('BLK', 'blk'))])],
 [('iv', [(OUT, '	for (blk = start, b = 0; b < blocks; b++, blk++) {\n')]),
  ('ie', [(OUT, '	blk = start;\n	for (b = 0; b < blocks; b++) {\n'),
          ('		}\n	}\n#undef BLK\n', '		}\n		blk++;\n	}\n#undef BLK\n')]),
  ('lo', [(OUT, OUT + '		blk = start + b;\n')]),
  ('li', [(INNER, INNER + '			blk = start + b;\n')]),
 ],
 [('', []), ('s2', [(SS, '			s = xb.spare + (pg + b * 32 + p) * 16;\n')])],
]
BASE = os.environ.get('IWB', 'build/iw/a6/r2.c')
FLAGS = []
