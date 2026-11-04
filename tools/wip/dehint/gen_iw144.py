# attempt 8: n8/n7 family: statements on `type` that fold at ccp2 in the type-0 clones shift which names the free list hands out later (`char t` flips constprop.1 and constprop.4 this way).
# Named temporaries on type and partial's pieces, IWB= base.
import os
FLAGS = []
BASE = os.environ.get('IWB', 'build/iw/a8/n8.c')
FOCUS = ['_imgAdd', '_imgAdd.constprop.1', '_imgAdd.constprop.2', '_imgAdd.constprop.4', '_imgAddFile', '_writeInitialHeader']
PA = "		partial = (len < 0x4000) & (type != 0) & (type != '0');\n"
DP = '	int partial;\n'
TL = "		t = type - '1';\n"
D = '	uint8_t t;\n'
C = 'if (t < 15) {'
A1 = [
 ('', []),
 ('p1', [(PA, "		small = (type != 0) & (type != '0');\n		partial = (len < 0x4000) & small;\n")]),
 ('p2', [(PA, "		small = type != 0 && type != '0';\n		partial = (len < 0x4000) & small;\n")]),
 ('p3', [(PA, "		small = type != 0;\n		small &= type != '0';\n		partial = (len < 0x4000) & small;\n")]),
 ('p4', [(PA, "		partial = len < 0x4000;\n		partial &= type != 0;\n		partial &= type != '0';\n")]),
 ('p5', [(PA, "		small = (len < 0x4000);\n		partial = small & (type != 0) & (type != '0');\n")]),
 ('p6', [(PA, "		partial = (len < 0x4000) & (_Bool)((type != 0) & (type != '0'));\n")]),
 ('p7', [(PA, "		partial = (len < 0x4000) ? (type != 0) & (type != '0') : 0;\n")]),
]
A2 = [
 ('', []),
 ('t1', [(TL, "		t = (uint8_t)type - '1';\n")]),
 ('t2', [(D, '	char t;\n'), (C, 'if ((uint8_t)t < 15) {')]),
 ('t3', [(TL, "		t = type;\n		t -= '1';\n")]),
 ('t4', [(D, '	int t;\n'), (TL, "		t = (uint8_t)(type - '1');\n")]),
 ('t5', [(D, '	unsigned t;\n'), (TL, "		t = (uint8_t)(type - '1');\n")]),
 ('t6', [(D, '	int t;\n'), (C, 'if ((uint8_t)t < 15) {')]),
]
TY1 = '					s[12] = (s[12] & 0xc0) | (type & 0x3f);\n					if (type != 0x2a'
TY2 = '					s[12] = (s[12] & 0xc0) | (type & 0x3f);\n					s[9] = 32 - pages;'
A3 = [
 ('', []),
 ('y1', [(TY1, '					sp9 = type & 0x3f;\n					s[12] = (s[12] & 0xc0) | sp9;\n					if (type != 0x2a')]),
 ('y2', [(TY2, '					sp9 = type & 0x3f;\n					s[12] = (s[12] & 0xc0) | sp9;\n					s[9] = 32 - pages;')]),
 ('y3', [(TY1, '					sp9 = type & 0x3f;\n					s[12] = (s[12] & 0xc0) | sp9;\n					if (type != 0x2a'), (TY2, '					sp9 = type & 0x3f;\n					s[12] = (s[12] & 0xc0) | sp9;\n					s[9] = 32 - pages;')]),
]
AXES = [A1, A2, A3]
