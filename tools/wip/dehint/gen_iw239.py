# attempt 17: pin_t on src: t's test spelled without the pin. Scored by lines; IWB=src/image_write.c. `no` is plain removal (10 lines), the rest change t's type, place or test.
import os
BASE = os.environ.get('IWB', 'src/image_write.c')
PIN = '''			/* no code: the slot order of t and partial (dead in every clone) */
			__asm__("" :: "g"(t));
'''
TD = '	uint8_t t;\n	uint32_t pg;\n'
T1 = "		t = type - '1';\n"
T2 = '		if (t < 15) {\n'
def form(lab, td, t1, t2):
    e = [(PIN, '')]
    if td is not None: e.append((TD, td))
    if t1 is not None: e.append((T1, t1))
    if t2 is not None: e.append((T2, t2))
    return (lab, e)
NOT = '	uint32_t pg;\n'
A = [form('no', None, None, None),
 form('r0', NOT, '', "		if (type >= '1' && type <= '?') {\n"),
 form('r1', NOT, '', "		if (type > '0' && type < '@') {\n"),
 form('r2', NOT, '', "		if ((uint8_t)(type - '1') < 15) {\n"),
 form('r3', NOT, '', "		if (type - '1' < 15u) {\n"),
 form('r4', NOT, '', "		if ((unsigned)(type - '1') < 15) {\n"),
 form('r5', NOT, '', "		if (!(type < '1' || type > '?')) {\n"),
 form('r6', NOT, '', "		if (type <= '?' && type >= '1') {\n"),
 form('r7', NOT, '', "		if (type > '0' && type <= '?') {\n"),
 form('r8', NOT, '', "		if (type >= '1' && type < '@') {\n"),
 form('t1', '	int t;\n	uint32_t pg;\n', "		t = type - '1';\n", "		if (t >= 0 && t < 15) {\n"),
 form('t2', '	uint32_t t;\n	uint32_t pg;\n', "		t = type - '1';\n", None),
 form('t3', '	int t;\n	uint32_t pg;\n', "		t = type - '1';\n", "		if ((uint32_t)t < 15) {\n"),
 form('t4', None, "", "		t = type - '1';\n		if (t < 15) {\n"),
]
AXES = [A]
FLAGS = []
