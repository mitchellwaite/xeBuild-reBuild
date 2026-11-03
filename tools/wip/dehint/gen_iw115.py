# attempt 6: f0: with or without blk, blk's position in the outer loop, and pg's form; the two big-copy compares want (r0's incr, f0's copy)
import os
BL = '		blk = start + b;\n		small = 0;\n'
U1 = '				((struct spb *)s)->b2lo = blk >> 8;\n'
PA = '		partial = small && len < 0x4000;\n'
T = "		t = type - '1';\n"
P0 = '		p = 0;\n'
PS = '			pg = start * 32;\n			s = xb.spare + (pg + p + b * 32) * 16;\n'
FE = '			fsTable[start - xb.fsStart + blocks - 1] = SWAP16_IMAGE_WRITE(0x1fff);\n'
WF = '	fsTable[blk - xb.fsStart] = SWAP16_IMAGE_WRITE(0x1ffd);\n'
AXES = [
 [('', []),
  ('nob', [(BL, '		small = 0;\n'), (U1, '				((struct spb *)s)->b2lo = BLK >> 8;\n')]),
  ('bp', [(BL, '		small = 0;\n'), (PA, PA + '		blk = start + b;\n')]),
  ('bt', [(BL, '		small = 0;\n'), (T, T + '		blk = start + b;\n')]),
  ('b0', [(BL, '		small = 0;\n'), (P0, '		blk = start + b;\n' + P0)]),
 ],
 [('', []),
  ('s1', [(PS, '			pg = start * 32;\n			s = xb.spare + (pg + b * 32 + p) * 16;\n')]),
  ('s3', [(PS, '			pg = start * 32;\n			pg += b * 32;\n			s = xb.spare + (pg + p) * 16;\n')]),
  ('s5', [(PS, '			pg = start * 32 + b * 32;\n			s = xb.spare + (pg + p) * 16;\n')]),
 ],
 [('', []), ('fo', [(FE, '			fsTable[start + blocks - 1 - xb.fsStart] = SWAP16_IMAGE_WRITE(0x1fff);\n')])],
 [('', []), ('wi', [(WF, '	i = blk - xb.fsStart;\n	fsTable[i] = SWAP16_IMAGE_WRITE(0x1ffd);\n')])],
]
BASE = os.environ.get('IWB', 'build/iw/a6/f0.c')
FLAGS = []
