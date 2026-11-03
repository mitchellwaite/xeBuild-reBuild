# attempt 6: f0 (2 lines): forms of small, partial, blk
import os
SM = "		small = 0;\n		if (type != 0 && type != '0')\n			small = 1;\n"
PA = '		partial = small && len < 0x4000;\n'
BL = '		blk = start + b;\n		small = 0;\n'
U1 = '				((struct spb *)s)->b2lo = blk >> 8;\n'
U3 = '				((struct sps *)s)->b1lo = BLK >> 8;\n'
D = '	_Bool small;\n'
AXES = [
 [('', []),
  ('h', [(SM, "		if (type != 0 && type != '0')\n			small = 1;\n		else\n			small = 0;\n")]),
  ('n', [(SM, "		small = 0;\n		if (type != 0)\n			if (type != '0')\n				small = 1;\n")]),
  ('z', [(SM, "		small = 1;\n		if (type == 0 || type == '0')\n			small = 0;\n")]),
  ('y', [(SM, "		if (type == 0 || type == '0')\n			small = 0;\n		else\n			small = 1;\n")]),
  ('q', [(SM, "		small = 0;\n		if ((type != 0) & (type != '0'))\n			small = 1;\n")]),
 ],
 [('', []),
  ('a', [(PA, '		partial = small & (len < 0x4000);\n')]),
  ('b', [(PA, '		partial = len < 0x4000 && small;\n')]),
  ('c', [(PA, '		partial = (len < 0x4000) & small;\n')]),
  ('d', [(PA, '		partial = 0;\n		if (small && len < 0x4000)\n			partial = 1;\n')]),
  ('e', [(PA, '		if (small && len < 0x4000)\n			partial = 1;\n		else\n			partial = 0;\n')]),
  ('f', [(PA, '		partial = small;\n		if (len >= 0x4000)\n			partial = 0;\n')]),
 ],
 [('u1', []), ('u13', [(U3, '				((struct sps *)s)->b1lo = blk >> 8;\n')]),
  ('u3', [(U1, '				((struct spb *)s)->b2lo = BLK >> 8;\n'), (U3, '				((struct sps *)s)->b1lo = blk >> 8;\n')]),
 ],
 [('', []), ('si', [(D, '	int small;\n')]), ('s8', [(D, '	uint8_t small;\n')])],
]
BASE = os.environ.get('IWB', 'build/iw/a6/f0.c')
FLAGS = []
