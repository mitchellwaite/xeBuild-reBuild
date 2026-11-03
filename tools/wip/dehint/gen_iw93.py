# attempt 6: on r0 (no dead tests, 2 lines): put dead tests back, any subset and body, for a first verified reduction
import os
LOOP = "		partial = (len < 0x4000) & (type != 0) & (type != '0');\n"
FS = '		for (i = 0; i < blocks; i++) {\n'
FILE = '	if (imgFits(off, len)) {\n		fsFiles'
AXES = [
 [('', []),
  ('A2', [(LOOP, '		if (x > first + 0x4000)\n			blocks += 2;\n' + LOOP)]),
  ('A2b', [(LOOP, '		if (x > first + 0x4000)\n			blocks++;\n' + LOOP)]),
  ('A2s', [(LOOP, '		if (x > first + 0x4000)\n			start++;\n' + LOOP)])],
 [('', []),
  ('C4', [(LOOP, '		if ((len & 0x3fff) > 0x3fff)\n			blocks++;\n' + LOOP)]),
  ('C4b', [(LOOP, '		if ((len & 0x3fff) > 0x3fff)\n			blocks += 2;\n' + LOOP)])],
 [('', []),
  ('A5', [(FS, FS + '			if (x > first + 0x4000)\n				blocks++;\n')]),
  ('A5b', [(FS, FS + '			if (x > first + 0x4000)\n				blocks += 2;\n')])],
 [('', []), ('LP', [(FILE, '	if ((len & 0x3fff) > 0x3fff)\n		len++;\n' + FILE)])],
]
BASE = os.environ.get('IWB', 'build/iw/a6/r0.c')
FLAGS = []
