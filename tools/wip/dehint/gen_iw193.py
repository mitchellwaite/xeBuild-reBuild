# attempt 12: guard freq in imgAddFile's clone = join - threaded edge, and folded type tests leave block freqs as the generic estimate had them. So forms where partial's false edge is split between type tests and the len test could raise the guard above 500 with no predictor. Axis 2: `if` spelling; axis 3: t's form (pin = keep pin_t, a net -1 reduction).
import os
BASE = os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_near11.c')
P0 = "		partial = (len < 0x4000) & (type != 0) & (type != '0');\n"
ARM = '''		if (partial) {
			if (len % 512)
				npages = (len + 512) / 512;
			else
				npages = len / 512;
		} else
			npages = 32;
'''
ARM2 = '''		if (!partial)
			npages = 32;
		else if (len % 512)
			npages = (len + 512) / 512;
		else
			npages = len / 512;
'''
TT = "		if ((uint8_t)t < 15) {\n"
A = [('', []),
 ('S1', [(P0, "		small = 0;\n		if (type != 0 && type != '0')\n			small = 1;\n		partial = small & (len < 0x4000);\n")]),
 ('S1b', [(P0, "		small = 0;\n		if (type != 0 && type != '0')\n			small = 1;\n		partial = small && len < 0x4000;\n")]),
 ('S2', [(P0, "		small = type != 0 && type != '0';\n		partial = small && len < 0x4000;\n")]),
 ('S3', [(P0, "		partial = 0;\n		if (len < 0x4000)\n			if (type != 0 && type != '0')\n				partial = 1;\n")]),
 ('S3b', [(P0, "		partial = 0;\n		if (type != 0 && type != '0')\n			if (len < 0x4000)\n				partial = 1;\n")]),
 ('S4', [(P0, "		partial = 1;\n		if (len >= 0x4000 || type == 0 || type == '0')\n			partial = 0;\n")]),
 ('S4b', [(P0, "		partial = 1;\n		if (type == 0 || type == '0' || len >= 0x4000)\n			partial = 0;\n")]),
 ('S5', [(P0, "		partial = 1;\n		if (type == 0 || type == '0')\n			partial = 0;\n		else if (len >= 0x4000)\n			partial = 0;\n")]),
 ('S6', [(P0, "		partial = type != 0 && type != '0' ? len < 0x4000 : 0;\n")]),
 ('S7', [(P0, "		partial = len < 0x4000;\n		if (type == 0 || type == '0')\n			partial = 0;\n")]),
 ('S8', [(P0, "		partial = len < 0x4000;\n		if (type == 0)\n			partial = 0;\n		if (type == '0')\n			partial = 0;\n")]),
 ('S9', [(P0, "		partial = len < 0x4000 && type != 0 && type != '0';\n")]),
 ('S10', [(P0, "		partial = type != 0 && type != '0' && len < 0x4000;\n")]),
 ('S11', [(P0, "		partial = len < 0x4000;\n		if (partial && (type == 0 || type == '0'))\n			partial = 0;\n")]),
 ('S12', [(P0, "		partial = len < 0x4000;\n		if (type == 0 || type == '0')\n			partial = 0;\n		else if (!partial)\n			partial = 0;\n")]),
]
B = [('', []), ('n', [(ARM, ARM2)])]
C = [('', []),
 ('pin', [('	unsigned t;\n', '	uint8_t t;\n'), (TT, '		if (t < 15) {\n			__asm__("" :: "g"(t));\n')]),
]
AXES = [A, B, C]
FLAGS = []
