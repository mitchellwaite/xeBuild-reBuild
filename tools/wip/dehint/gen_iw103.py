# attempt 6: pin on t gone: the test written as a range on type (t < 15 is type - '1' < 15), so ifcombine or fold makes t
import os
T = "		t = type - '1';\n"
I = '''		if (t < 15) {
			/* no code: the slot order of t and partial (dead in every clone) */
			__asm__("" :: "g"(t));
'''
F = {
 'pin': None,
 'nopin': (T, '		if (t < 15) {\n'),
 'r1': ('', "		if (type >= '1' && type < '@') {\n"),
 'r2': ('', "		if (type > '0' && type <= '?') {\n"),
 'r3': ('', "		if (type >= 0x31 && type <= 0x3f) {\n"),
 'r4': ('', "		if (type <= '?' && type >= '1') {\n"),
 'r5': ('', "		if (type > 0x30 && type < 0x40) {\n"),
 'r6': ('', "		if ((uint8_t)(type - '1') < 15) {\n"),
 'r7': ('', "		if (type - '1' >= 0 && type - '1' < 15) {\n"),
 'r8': ('', "		if ((type >> 4) == 3 && type != '0') {\n"),
 'r9': (T, '		if (t <= 14) {\n'),
 'r10': ("		t = type - 0x31;\n", '		if (t < 0xf) {\n'),
}
AXES = [
 [(k, [] if v is None else [(T, v[0]), (I, v[1])]) for k, v in F.items()],
 [('', []), ('ch', [("		partial = (len < 0x4000) & (type != 0) & (type != '0');\n", "		partial = type != 0 && type != '0' && len < 0x4000;\n")])],
]
BASE = os.environ.get('IWB', 'build/iw/a6/r0.c')
FLAGS = []
