# attempt 5: the c10/c11 family (no dead test in imgAddFile): dead-test bodies and presence x small's form x writeFsTable's first store
import os
BASE = os.environ.get('IWB', 'build/iw/a5/c10.c')
C4 = '		if ((len & 0x3fff) > 0x3fff)\n			blocks++;\n'
A2 = '		if (x > first + 0x4000)\n			blocks += 2;\n'
A5 = '			if (x > first + 0x4000)\n				blocks++;\n'
S = "		partial = 0;\n		small = type != 0 && type != '0';\n		if (small && len < 0x4000)\n			partial = 1;\n"
ST = '	fsTable[blk - xb.fsStart] = SWAP16_IMAGE_WRITE(0x1ffd);\n'
AXES = [
 [('', []), ('c4x', [(C4, '')]), ('c4b', [(C4, '		if ((len & 0x3fff) > 0x3fff)\n			blocks += 2;\n')]), ('c4s', [(C4, '		if ((len & 0x3fff) > 0x3fff)\n			start++;\n')])],
 [('', []), ('a21', [(A2, '		if (x > first + 0x4000)\n			blocks++;\n')]), ('a2s', [(A2, '		if (x > first + 0x4000)\n			start++;\n')])],
 [('', []), ('a52', [(A5, '			if (x > first + 0x4000)\n				blocks += 2;\n')]), ('a5s', [(A5, '			if (x > first + 0x4000)\n				start++;\n')])],
 [('', []), ('sb', [('	int small;\n', '	_Bool small;\n')]), ('s8', [('	int small;\n', '	uint8_t small;\n')])],
 [('', []),
  ('f1', [(S, "		small = type != 0 && type != '0';\n		partial = 0;\n		if (small && len < 0x4000)\n			partial = 1;\n")]),
  ('f2', [(S, "		small = type != 0 && type != '0';\n		if (small && len < 0x4000)\n			partial = 1;\n		else\n			partial = 0;\n")]),
 ],
 [('', []), ('i', [(ST, '	i = blk - xb.fsStart;\n	fsTable[i] = SWAP16_IMAGE_WRITE(0x1ffd);\n')])],
]
FLAGS = []
