# attempt 6: d0 (writeFsTable right; constprop.2's compares and imgAdd's t lea and two byte slots left): t's position, partial family, pages, big-arm test
import os
PART = "		partial = (type != 0) & (type != '0') && len < 0x4000;\n"
T = "		t = type - '1';\n"
NP = '		if (len % 512)\n			npages = (len + 512) / 512;\n'
P0 = '		p = 0;\n'
PG = '			pages = len % 512 ? len / 512 + 1 : len / 512;\n'
TY = "					if (type != 0x2a && type != 0x2c) {\n"
AXES = [
 [('', []),
  ('tf', [(PART + T, T + PART)]),
  ('tp', [(T, ''), (P0, T + P0)]),
 ],
 [('', []),
  ('f2', [(PART, "		partial = type != 0 && type != '0' ? len < 0x4000 : 0;\n")]),
  ('f17', [(PART, "		partial = (type != 0 && type != '0') && (len < 0x4000);\n")]),
  ('f18', [(PART, "		partial = ((type != 0) & (type != '0')) ? len < 0x4000 : 0;\n")]),
  ('f19', [(PART, "		partial = (type != '0') & (type != 0) && len < 0x4000;\n")]),
  ('f20', [(PART, "		partial = (type != 0) && (type != '0') && len < 0x4000;\n")]),
 ],
 [('', []), ('pg1', [(PG, '			pages = len / 512 + (len % 512 ? 1 : 0);\n')]),
  ('pg2', [(PG, '			pages = len / 512;\n			if (len % 512)\n				pages++;\n')])],
 [('', []), ('ty', [(TY, "					if (type != 0x2c && type != 0x2a) {\n")]),
  ('tz', [(TY, "					if ((type & ~2) != 0x2a) {\n")])],
]
BASE = os.environ.get('IWB', 'build/iw/a6/d0.c')
FLAGS = []
