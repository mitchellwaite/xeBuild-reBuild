# attempt 6: r1: one off-only statement in the inner loop that leaves BLK * 32 alone: s[9]'s `off & 0x1ffff` as a local, up front like `pages`
import os
S9 = '						s[9] = (((off & 0x1ffff) ? 256 - (off & 0x1ffff) / 512 : 256) - left) >> 2;\n'
PAGES = '			pages = len % 512 ? len / 512 + 1 : len / 512;\n'
MS = '			memset(s, 0, 16);\n			if (xb.bigBlock) {\n				((struct spb'
SS = '			s = xb.spare + (BLK * 32 + p) * 16;\n'
PART = "		partial = (len < 0x4000) & (type != 0) & (type != '0');\n"
USE = '						s[9] = ((pg ? 256 - pg / 512 : 256) - left) >> 2;\n'
D = 'pg = off & 0x1ffff;\n'
USE2 = '						s[9] = ((pg ? 256 - (off & 0x1ffff) / 512 : 256) - left) >> 2;\n'
AXES = [
 [('s', [(SS, '			' + D + SS), (S9, USE)]),
  ('ps', [(PAGES, '			' + D + PAGES), (S9, USE)]),
  ('pa', [(PAGES, PAGES + '			' + D), (S9, USE)]),
  ('m', [(MS, '			memset(s, 0, 16);\n			' + D + '			if (xb.bigBlock) {\n				((struct spb'), (S9, USE)]),
  ('s2', [(SS, '			' + D + SS), (S9, USE2)]),
  ('ps2', [(PAGES, '			' + D + PAGES), (S9, USE2)]),
 ],
 [('', []),
  ('pb', [(PART, "		partial = type != 0 && type != '0' && len < 0x4000;\n")]),
  ('pa', [(PART, "		partial = len < 0x4000 && type != 0 && type != '0';\n")])],
]
BASE = os.environ.get('IWB', 'build/iw/a6/r1.c')
FLAGS = []
