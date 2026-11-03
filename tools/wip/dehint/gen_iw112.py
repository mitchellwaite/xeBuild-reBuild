# attempt 6: e0/c1 (IWB=): partial through a `small` temporary (attempt 5's lever: a copy released late sets which low name ifcombine pops, so t's lea order)
import os
PART = "		partial = (type != 0) & (type != '0') && len < 0x4000;\n"
D = '	int partial;\n'
F = {
 'a': "small = (type != 0) & (type != '0');\n		partial = small && len < 0x4000;\n",
 'b': "small = type != 0 && type != '0';\n		partial = small && len < 0x4000;\n",
 'c': "small = type != 0 && type != '0';\n		partial = small & (len < 0x4000);\n",
 'd': "small = (type != 0) & (type != '0');\n		partial = small & (len < 0x4000);\n",
 'e': "small = 0;\n		if (type != 0 && type != '0')\n			small = 1;\n		partial = small && len < 0x4000;\n",
 'f': "small = 0;\n		if ((type != 0) & (type != '0'))\n			small = 1;\n		partial = small && len < 0x4000;\n",
 'g': "small = 0;\n		if (type != 0 && type != '0')\n			small = 1;\n		partial = small & (len < 0x4000);\n",
 'h': "if (type != 0 && type != '0')\n			small = 1;\n		else\n			small = 0;\n		partial = small && len < 0x4000;\n",
 'i': "small = type != 0 && type != '0';\n		if (small && len < 0x4000)\n			partial = 1;\n		else\n			partial = 0;\n",
 'j': "small = (type != 0) & (type != '0');\n		if (small && len < 0x4000)\n			partial = 1;\n		else\n			partial = 0;\n",
}
AXES = [
 [(k, [(PART, '		' + v)]) for k, v in F.items()],
 [('bi', [(D, D + '	_Bool small;\n')]), ('ii', [(D, D + '	int small;\n')]),
  ('bb', [(D, '	_Bool partial, small;\n')]), ('ib', [(D, '	_Bool partial;\n	int small;\n')])],
]
BASE = os.environ.get('IWB', 'build/iw/a6/e0.c')
FLAGS = []
