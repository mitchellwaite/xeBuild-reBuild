# attempt 5: c12: partial's and small's forms and types x writeFsTable's store and setBeU16 forms
import os
BASE = os.environ.get('IWB', 'build/iw/a5/c12.c')
S1 = "		small = type != 0 && type != '0';\n"
S2 = "		if (small && len < 0x4000)\n			partial = 1;\n		else\n			partial = 0;\n"
AXES = [
 [('', []),
  ('s1', [(S1, "		small = type != '0' && type != 0;\n")]),
  ('s2', [(S1, "		small = type && type != '0';\n")]),
  ('s3', [(S1, "		small = !(type == 0 || type == '0');\n")]),
  ('s4', [(S1, "		small = type != 0;\n		small = small && type != '0';\n")]),
  ('s5', [(S1, "		small = 0;\n		if (type != 0 && type != '0')\n			small = 1;\n")]),
  ('s6', [(S1, "		small = (type != 0) & (type != '0');\n")]),
 ],
 [('', []),
  ('p1', [(S2, "		if (!small || len >= 0x4000)\n			partial = 0;\n		else\n			partial = 1;\n")]),
  ('p2', [(S2, "		partial = 0;\n		if (small)\n			if (len < 0x4000)\n				partial = 1;\n")]),
  ('p3', [(S2, "		partial = small && len < 0x4000 ? 1 : 0;\n")]),
  ('p4', [(S2, "		partial = small ? len < 0x4000 : 0;\n")]),
  ('p5', [(S2, "		if (small)\n			partial = len < 0x4000;\n		else\n			partial = 0;\n")]),
  ('p6', [(S2, "		if (len < 0x4000 && small)\n			partial = 1;\n		else\n			partial = 0;\n")]),
  ('p7', [(S2, "		partial = small && len < 0x4000;\n")]),
 ],
 [('', []), ('pi', [('	_Bool partial;\n', '	int partial;\n')]), ('p8', [('	_Bool partial;\n', '	uint8_t partial;\n')])],
 [('', []), ('sb', [('	int small;\n', '	_Bool small;\n')]), ('s8', [('	int small;\n', '	uint8_t small;\n')])],
 [('', []), ('t2', [('	setBeU16(blk, (uint8_t *)&xb.fsBlock);\n', '	setBeU16(off >> 14, (uint8_t *)&xb.fsBlock);\n')])],
]
FLAGS = []
