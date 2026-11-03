# attempt 5: c13: more forms of small and partial together, x writeFsTable's first store, x npages form
import os
BASE = os.environ.get('IWB', 'build/iw/a5/c13.c')
S = "		small = 0;\n		if (type != 0 && type != '0')\n			small = 1;\n"
P = "		partial = small && len < 0x4000;\n"
ST = '	i = blk - xb.fsStart;\n	fsTable[i] = SWAP16_IMAGE_WRITE(0x1ffd);\n'
NP = '		if (len % 512)\n			npages = (len + 512) / 512;\n		else\n			npages = len / 512;\n'
AXES = [
 [('', []),
  ('s1', [(S, "		small = 1;\n		if (type == 0 || type == '0')\n			small = 0;\n")]),
  ('s2', [(S, "		if (type != 0 && type != '0')\n			small = 1;\n		else\n			small = 0;\n")]),
  ('s3', [(S, "		if (type == 0 || type == '0')\n			small = 0;\n		else\n			small = 1;\n")]),
  ('s4', [(S, "		small = 1;\n		if (type == 0)\n			small = 0;\n		if (type == '0')\n			small = 0;\n")]),
  ('s5', [(S, "		small = 0;\n		if (type != 0)\n			small = type != '0';\n")]),
  ('s6', [(S, "		small = 0;\n		if (type != '0')\n			small = type != 0;\n")]),
  ('s7', [(S, "		small = type != 0;\n		if (type == '0')\n			small = 0;\n")]),
  ('s8', [(S, "		small = type != '0';\n		if (type == 0)\n			small = 0;\n")]),
 ],
 [('', []),
  ('p1', [(P, "		partial = len < 0x4000 && small;\n")]),
  ('p2', [(P, "		partial = small & (len < 0x4000);\n")]),
  ('p3', [(P, "		partial = (len < 0x4000) & small;\n")]),
  ('p4', [(P, "		partial = 0;\n		if (small && len < 0x4000)\n			partial = 1;\n")]),
  ('p5', [(P, "		partial = 0;\n		if (len < 0x4000)\n			partial = small;\n")]),
  ('p6', [(P, "		partial = small;\n		if (len >= 0x4000)\n			partial = 0;\n")]),
  ('p7', [(P, "		partial = len < 0x4000 ? small : 0;\n")]),
 ],
 [('', []),
  ('w1', [(ST, '	fsTable[blk - xb.fsStart] = SWAP16_IMAGE_WRITE(0x1ffd);\n')]),
 ],
 [('', []),
  ('sp', [('	_Bool small;\n', '	uint8_t small;\n')]),
  ('pp', [('	int partial;\n', '	uint32_t partial;\n')]),
 ],
]
FLAGS = []
