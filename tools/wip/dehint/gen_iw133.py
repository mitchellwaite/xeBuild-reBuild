# attempt 8: pages computed in the type arms (no inline of writeInitialHeader's call): where in the arms x partial forms x t forms x npages forms.
# Base build/iw/a8/n3.c = gen_iw132 `arm`.
import os
FLAGS = []
BASE = os.environ.get('IWB', 'build/iw/a8/n3.c')
FOCUS = ['_imgAdd', '_imgAdd.constprop.1', '_imgAdd.constprop.2', '_imgAdd.constprop.4', '_imgAddFile', '_writeInitialHeader']
PG = '					pages = len % 512 ? len / 512 + 1 : len / 512;\n'
PG2 = '				pages = len % 512 ? len / 512 + 1 : len / 512;\n'
B0 = '				if (type > 1) {\n' + PG + '					s[12] = (s[12] & 0xc0) | (type & 0x3f);\n					if (type != 0x2a && type != 0x2c) {\n						left = pages;\n'
S0 = '					s[12] = (s[12] & 0xc0) | (type & 0x3f);\n' + PG + '					s[9] = 32 - pages;\n'
BF = [
 ('', []),
 ('b1', [(B0, '				if (type > 1) {\n					s[12] = (s[12] & 0xc0) | (type & 0x3f);\n					if (type != 0x2a && type != 0x2c) {\n						pages = len % 512 ? len / 512 + 1 : len / 512;\n						left = pages;\n')]),
 ('b2', [(B0, '				if (type > 1) {\n					s[12] = (s[12] & 0xc0) | (type & 0x3f);\n					if (type != 0x2a && type != 0x2c) {\n						left = len % 512 ? len / 512 + 1 : len / 512;\n')]),
 ('b3', [(B0, '				if (type > 1) {\n					s[12] = (s[12] & 0xc0) | (type & 0x3f);\n					if (type != 0x2a && type != 0x2c) {\n						left = len / 512;\n						if (len % 512)\n							left++;\n')]),
]
SF = [
 ('', []),
 ('s1', [(S0, '					s[12] = (s[12] & 0xc0) | (type & 0x3f);\n					s[9] = 32 - (len % 512 ? len / 512 + 1 : len / 512);\n')]),
 ('s2', [(S0, '					pages = len % 512 ? len / 512 + 1 : len / 512;\n					s[12] = (s[12] & 0xc0) | (type & 0x3f);\n					s[9] = 32 - pages;\n')]),
]
P = "		partial = (len < 0x4000) & (type != 0) & (type != '0');\n"
PF = [
 ('p1', []),
 ('p2', [(P, "		partial = type != 0 && type != '0' && len < 0x4000;\n")]),
 ('p3', [(P, "		small = 0;\n		if (type != 0 && type != '0')\n			small = 1;\n		partial = small && len < 0x4000;\n")]),
]
TD = '	unsigned t;\n'
TC = 'if ((uint8_t)t < 15) {'
TF = [('ti', []), ('tb', [(TD, '	uint8_t t;\n'), (TC, 'if (t < 15) {')])]
AXES = [BF, SF, PF, TF]
