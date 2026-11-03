# attempt 6: `start` not computed up front, but in each loop: a time benefit on off in the spare loop
# that FRE1 can't merge (neither def dominates the other), PRE hoists later.  a2/a5 gone or kept.
A2 = '		if (x > first + 0x4000)\n			blocks += 2;\n'
C4 = '		if ((len & 0x3fff) > 0x3fff)\n			blocks++;\n'
A5 = '			if (x > first + 0x4000)\n				blocks++;\n'
ST = '	start = (off - x) >> 14;\n'
BLK = '#define BLK (start + b)\n'
FST = '''		for (i = 0; i < blocks; i++) {
'''
AXES = [
 [('a2', [(A2, '')]), ('', [])],
 [('a5', [(A5, '')]), ('', [])],
 [('c4', [(C4, '')]), ('', [])],
 [('sL', [(ST, ''),
          ('	for (b = 0; b < blocks; b++) {\n', '	for (b = 0; b < blocks; b++) {\n		start = (off - x) >> 14;\n'),
          ('	if (next != 0xf1f1) {\n\n', '	if (next != 0xf1f1) {\n		start = (off - x) >> 14;\n')]),
  ('sB', [(ST, ''), (BLK, '#define BLK (((off - x) >> 14) + b)\n'),
          ('	if (next != 0xf1f1) {\n\n', '	if (next != 0xf1f1) {\n		start = (off - x) >> 14;\n')]),
  ('sI', [(ST, ''), (BLK, '#define BLK (((off - x) >> 14) + b)\n'),
          (FST, FST + '			start = (off - x) >> 14;\n'),
          ('		if (next == 0xffff) {\n', '		start = (off - x) >> 14;\n		if (next == 0xffff) {\n')]),
  ('sP', [(ST, ''), (BLK, '#define BLK ((off - x) / 0x4000 + b)\n'),
          ('	if (next != 0xf1f1) {\n\n', '	if (next != 0xf1f1) {\n		start = (off - x) >> 14;\n')]),
  ],
]
BASE = 'src/image_write.c'
FLAGS = []
