# attempt 10: pin_t gone on src.  Pin off costs imgAdd 10 lines: t and partial's byte slots (r235 t total 178, r234 partial 180).  Lower partial's total or raise t's:
# forms of partial x its type x where t is computed.  Good: total 0.
import os
PIN = '''			/* no code: the slot order of t and partial (dead in every clone) */
			__asm__("" :: "g"(t));
'''
P0 = '		partial = small && len < 0x4000;\n'
PF = {
 '': P0,
 'p1': '		partial = 0;\n		if (small && len < 0x4000)\n			partial = 1;\n',
 'p2': '		if (small && len < 0x4000)\n			partial = 1;\n		else\n			partial = 0;\n',
 'p3': '		partial = len < 0x4000 && small;\n',
 'p4': '		partial = small & (len < 0x4000);\n',
 'p5': '		partial = small ? len < 0x4000 : 0;\n',
 'p6': '		partial = 0;\n		if (small)\n			partial = len < 0x4000;\n',
 'p7': '		partial = small;\n		if (len >= 0x4000)\n			partial = 0;\n',
 'p8': '		partial = small;\n		if (partial && len >= 0x4000)\n			partial = 0;\n',
 'p9': '		partial = len < 0x4000;\n		if (!small)\n			partial = 0;\n',
}
TY = {
 '': [],
 'B': [('	int partial;\n', '	_Bool partial;\n')],
 'U': [('	int partial;\n', '	unsigned partial;\n')],
}
T0 = "		t = type - '1';\n"
TEST = '		if (t < 15) {\n'
TF = {
 '': [],
 'tb': [(T0, ''), ('		p = 0;\n' + TEST, "		p = 0;\n		t = type - '1';\n" + TEST)],
 'tt': [(T0, ''), ('		blk = start + b;\n', "		blk = start + b;\n		t = type - '1';\n")],
 'tp': [(T0, ''), ('		small = 0;\n', "		t = type - '1';\n		small = 0;\n")],
 'tu': [('	uint8_t t;\n', '	unsigned t;\n'), (TEST, '		if ((uint8_t)t < 15) {\n')],
 'tn': [(T0, ''), (TEST, "		if ((uint8_t)(type - '1') < 15) {\n"), ('	uint8_t t;\n', '')],
}
AXES = [
 [('nopin', [(PIN, '')])],
 [(k, [(P0, v)]) for k, v in PF.items()],
 [(k, v) for k, v in TY.items()],
 [(k, v) for k, v in TF.items()],
]
BASE = os.environ.get('IWB', 'src/image_write.c')
FLAGS = []
