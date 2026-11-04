# attempt 11: on near11 (g3).  imgAddFile's slots want P(partial) >= 55%; the one predictor is `partial > 0` (73%), and that spelling flips imgAddFile's compare or constprop.4's lea (VRP rewrites it; attempt 8).  Partial's type x spelling x t's type.
import os
BASE = os.environ.get('IWB', 'build/iw/a11/g3.c')
D = '	int partial;\n'
PA = "		partial = (len < 0x4000) & (type != 0) & (type != '0');\n"
IF = '		if (partial) {\n'
TD = '	unsigned t;\n'
C = '		if ((uint8_t)t < 15) {\n'
E0 = '		} else\n			npages = 32;\n'
AXES = [
 [(k, [(D, '	%s partial;\n' % k)] if k != 'int' else []) for k in ('int', 'short', 'signed char', 'long', 'long long')],
 [('', []), ('pc', [(PA, "		partial = (int)(len < 0x4000) & (int)(type != 0) & (int)(type != '0');\n")]),
  ('ps', [(PA, "		partial = len < 0x4000 && type != 0 && type != '0';\n")]),
  ('pt', [(PA, "		partial = 0;\n		if (len < 0x4000 && type != 0 && type != '0')\n			partial = 1;\n")]),
  ('pq', [(PA, "		partial = (len < 0x4000 && type != 0 && type != '0') ? 1 : 0;\n")]),
  ('pm', [(PA, "		partial = (len < 0x4000) * (type != 0) * (type != '0');\n")]),
  ('pd', [(PA, "		partial = 0x4000 - len;\n		partial = type != 0 && type != '0' ? partial : 0;\n")]),
 ],
 [('gt', [(IF, '		if (partial > 0) {\n')]),
  ('ge', [(IF, '		if (partial >= 1) {\n')]),
 ],
 [('', []), ('tch', [(TD, '	char t;\n')]), ('tin', [(TD, '	int t;\n')]), ('tu8', [(TD, '	uint8_t t;\n'), (C, '		if (t < 15) {\n')])],
]
FLAGS = []
FOCUS = ['_imgAdd', '_imgAdd.constprop.1', '_imgAdd.constprop.2', '_imgAdd.constprop.4', '_imgAddFile', '_writeInitialHeader']
