# attempt 8: n8: `small` set by an if (as in src), but no short circuit on len, so no extra branch for the predictors.
import os
FLAGS = []
BASE = os.environ.get('IWB', 'build/iw/a8/n8.c')
FOCUS = ['_imgAdd', '_imgAdd.constprop.1', '_imgAdd.constprop.2', '_imgAdd.constprop.4', '_imgAddFile', '_writeInitialHeader']
PA = "		partial = (len < 0x4000) & (type != 0) & (type != '0');\n"
S1 = "		small = 0;\n		if (type != 0 && type != '0')\n			small = 1;\n"
S2 = "		if (type != 0 && type != '0')\n			small = 1;\n		else\n			small = 0;\n"
S3 = "		small = type != 0 && type != '0';\n"
S4 = "		small = 1;\n		if (type == 0 || type == '0')\n			small = 0;\n"
S5 = "		small = 0;\n		if (type != 0)\n			if (type != '0')\n				small = 1;\n"
SS = [('s1', S1), ('s2', S2), ('s3', S3), ('s4', S4), ('s5', S5)]
TT = [('a', "		partial = small & (len < 0x4000);\n"), ('b', "		partial = (len < 0x4000) & small;\n"), ('c', "		partial = small;\n		partial &= len < 0x4000;\n"),
      ('d', "		partial = len < 0x4000;\n		partial &= small;\n")]
A = [('', [])]
for sn, s in SS:
    for tn, t in TT:
        A.append((sn + tn, [(PA, s + t)]))
DT = [('', []), ('dint', [('	_Bool small;\n', '	int small;\n')]), ('du8', [('	_Bool small;\n', '	uint8_t small;\n')])]
PG = [('', []), ('n7', [('						pages = len / 512;\n						if (len % 512)\n							pages++;\n', '						pages = len % 512 ? len / 512 + 1 : len / 512;\n')])]
AXES = [A, DT, PG]
