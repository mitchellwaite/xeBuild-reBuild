# attempt 6: c2 (IWB=, default; blk local for s[1], s[0], pg, `&` partial, no dead tests, 10 lines): where blk is set and used, where pg is, small forms
import os
OUTL = '	for (b = 0; b < blocks; b++) {\n		blk = start + b;\n'
OUT0 = '	for (b = 0; b < blocks; b++) {\n'
U1 = '				((struct spb *)s)->b2lo = BLK >> 8;\n'
U3 = '				((struct sps *)s)->b1lo = BLK >> 8;\n'
PS = '			pg = start * 32;\n			s = xb.spare + (pg + p + b * 32) * 16;\n'
INNER = '		for (end = p + npages; p < end; p++) {\n'
P0 = '		p = 0;\n'
PART = "		partial = (len < 0x4000) & (type != 0) & (type != '0');\n"
T = "		t = type - '1';\n"
AXES = [
 [('', []),
  ('lP', [(OUTL, OUT0), (P0, '		blk = start + b;\n' + P0)]),
  ('lI', [(OUTL, OUT0), (INNER, '		blk = start + b;\n' + INNER)]),
  ('lT', [(OUTL, OUT0), (T, T + '		blk = start + b;\n')]),
  ('lB', [(OUTL, OUT0 + "		blk = b + start;\n")]),
 ],
 [('', []), ('u1', [(U1, U1.replace('BLK', 'blk'))]), ('u3', [(U3, U3.replace('BLK', 'blk'))])],
 [('', []),
  ('s1', [(PS, '			pg = start * 32;\n			s = xb.spare + (pg + b * 32 + p) * 16;\n')]),
  ('s2', [(PS, '			pg = start * 32;\n			s = xb.spare + (b * 32 + pg + p) * 16;\n')]),
  ('s3', [(PS, '			pg = start * 32;\n			pg += b * 32;\n			s = xb.spare + (pg + p) * 16;\n')]),
  ('s4', [(PS, '			pg = 32 * start;\n			s = xb.spare + (pg + p + 32 * b) * 16;\n')]),
 ],
 [('', []),
  ('p12', [(PART, "		partial = (type != 0) & (type != '0') & (len < 0x4000);\n")]),
  ('p13', [(PART, "		partial = (type != 0) & (len < 0x4000) & (type != '0');\n")]),
  ('p14', [(PART, "		partial = (len < 0x4000) & ((type != 0) & (type != '0'));\n")])],
]
BASE = os.environ.get('IWB', 'build/iw/a6/c2.c')
FLAGS = []
