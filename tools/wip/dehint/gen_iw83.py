# attempt 5: c13 (one compare off in writeFsTable): dead test bodies x small's test forms x t forms x writeFsTable's length arguments
import os
BASE = os.environ.get('IWB', 'build/iw/a5/c13.c')
C4 = '		if ((len & 0x3fff) > 0x3fff)\n			blocks++;\n'
A2 = '		if (x > first + 0x4000)\n			blocks += 2;\n'
A5 = '			if (x > first + 0x4000)\n				blocks++;\n'
S = "		if (type != 0 && type != '0')\n			small = 1;\n"
T = "		t = type - '1';\n"
AXES = [
 [('', []), ('c4x', [(C4, '')]), ('c4b', [(C4, '		if ((len & 0x3fff) > 0x3fff)\n			blocks += 2;\n')])],
 [('', []), ('a21', [(A2, '		if (x > first + 0x4000)\n			blocks++;\n')]), ('a2s', [(A2, '		if (x > first + 0x4000)\n			start++;\n')])],
 [('', []), ('a52', [(A5, '			if (x > first + 0x4000)\n				blocks += 2;\n')]), ('a5s', [(A5, '			if (x > first + 0x4000)\n				start++;\n')])],
 [('', []),
  ('n1', [(S, "		if (type != 0)\n			if (type != '0')\n				small = 1;\n")]),
  ('n2', [(S, "		if (type != '0' && type != 0)\n			small = 1;\n")]),
  ('n3', [(S, "		if (type && type != '0')\n			small = 1;\n")]),
  ('n4', [(S, "		if (type != 0 && type != '0') {\n			small = 1;\n		}\n")]),
 ],
 [('', []), ('t1', [(T, "		t = (uint8_t)(type - '1');\n")]), ('t3', [(T, "		t = type;\n		t -= '1';\n")])],
 [('', []),
  ('w1', [('	imgAdd(off, buf, i * 0x400, 0x2c, 0x1ffe, 0);\n', '	imgAdd(off, buf, 0x4000, 0x2c, 0x1ffe, 0);\n')]),
  ('w2', [('	imgAdd(off, buf, i * 0x400, 0x2c, 0x1ffe, 0);\n', '	imgAdd(off, buf, p - buf, 0x2c, 0x1ffe, 0);\n')]),
 ],
]
FLAGS = []
