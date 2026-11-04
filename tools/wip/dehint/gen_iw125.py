# attempt 7: lnp2 gone (n1+p1 on a7): writeInitialHeader inlines the off-0x80 clone because inlining saves just over 10% (big_speedup, 3569 -> 3206): natural temporaries in the loops raise the time, or a form saves less
import os
S = '''			pg = start * 32;
			s = xb.spare + (pg + p + b * 32) * 16;
'''
D0 = '	uint32_t pg;\n'
PG = '			pages = len % 512 ? len / 512 + 1 : len / 512;\n'
MS = '			memset(s, 0, 16);\n'
AXES = [
 [('', []),
  ('s1', [(D0, D0 + '	uint32_t bp;\n'), (S, '			pg = start * 32;\n			bp = b * 32;\n			s = xb.spare + (pg + p + bp) * 16;\n')]),
  ('s2', [(D0, D0 + '	uint32_t bp;\n'), (S, '			pg = start * 32;\n			bp = b * 32 + p;\n			s = xb.spare + (pg + bp) * 16;\n')]),
  ('s3', [(D0, D0 + '	uint32_t bp;\n'), (S, '			pg = start * 32;\n			bp = pg + p + b * 32;\n			s = xb.spare + bp * 16;\n')]),
  ('s4', [(D0, D0 + '	uint32_t bp;\n'), (S, '			pg = start * 32;\n			bp = (pg + p + b * 32) * 16;\n			s = xb.spare + bp;\n')]),
  ('s5', [(D0, D0 + '	uint8_t *sp;\n'), (S, '			pg = start * 32;\n			sp = xb.spare;\n			s = sp + (pg + p + b * 32) * 16;\n')]),
 ],
 [('', []),
  ('g1', [(PG, '			pages = len / 512;\n			if (len % 512)\n				pages++;\n')]),
  ('g2', [(PG, '			if (len % 512)\n				pages = len / 512 + 1;\n			else\n				pages = len / 512;\n')]),
  ('g3', [(PG, '			pages = (len + 511) / 512;\n')]),
 ],
 [('', []),
  ('m1', [(MS, '			s[0] = s[1] = s[2] = s[3] = 0;\n			memset(s + 4, 0, 12);\n')]),
 ],
]
BASE = os.environ.get('IWB', 'build/iw/a7/n1p1.c')
FLAGS = []
FOCUS = ['_imgAdd', '_imgAdd.constprop.1', '_imgAdd.constprop.2', '_imgAdd.constprop.4', '_imgAddFile', '_imgAddFileAs', '_imgAddMobile', '_addSmcConfig', '_writeInitialHeader']
