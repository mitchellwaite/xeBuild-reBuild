# attempt 6: on q1 (no dead tests, 18 lines): put dead tests back, any subset, for a first verified reduction
LOOP = '		partial = len < 0x4000 && type != 0 && type != \'0\';\n'
FS = '		for (i = 0; i < blocks; i++) {\n'
FILE = '	uint32_t off = imgSizeAligned();\n\n	if (imgFits(off, len)) {\n		fsFiles'
AXES = [
 [('', []), ('A2', [(LOOP, '		if (x > first + 0x4000)\n			blocks += 2;\n' + LOOP)])],
 [('', []), ('C4', [(LOOP, '		if ((len & 0x3fff) > 0x3fff)\n			blocks++;\n' + LOOP)])],
 [('', []), ('A5', [(FS, FS + '			if (x > first + 0x4000)\n				blocks++;\n')])],
 [('', []), ('LP', [(FILE, '	uint32_t off = imgSizeAligned();\n\n	if ((len & 0x3fff) > 0x3fff)\n		len++;\n	if (imgFits(off, len)) {\n		fsFiles')])],
]
BASE = 'build/iw/a6/q1.c'
FLAGS = []
