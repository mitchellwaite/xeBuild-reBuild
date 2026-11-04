# attempt 8: from n7: t's type moves constprop.1's and constprop.4's compares (one each): t forms x pages positions, with and without the pin.
import os
FLAGS = []
BASE = os.environ.get('IWB', 'build/iw/a8/n7.c')
FOCUS = ['_imgAdd', '_imgAdd.constprop.1', '_imgAdd.constprop.2', '_imgAdd.constprop.4', '_imgAddFile', '_writeInitialHeader']
D = '	uint8_t t;\n'
C = 'if (t < 15) {'
S = "t = type - '1';"
PIN = '			__asm__("" :: "g"(t));\n'
TY = [
 ('', []),
 ('ui', [(D, '	unsigned t;\n'), (C, 'if ((uint8_t)t < 15) {')]),
 ('in', [(D, '	int t;\n'), (C, 'if ((uint8_t)t < 15) {')]),
 ('ch', [(D, '	char t;\n'), (C, 'if ((uint8_t)t < 15) {')]),
 ('u16', [(D, '	uint16_t t;\n'), (C, 'if ((uint8_t)t < 15) {')]),
 ('c2', [(S, "t = type; t -= '1';")]),
 ('c3', [(S, "t = (uint8_t)type - (uint8_t)'1';")]),
 ('c4', [(S, "t = (uint8_t)(type - 0x31u);")]),
 ('c5', [(S, "t = type + 0xcf;")]),
]
PN = [('pin', []), ('nop', [(PIN, '')])]
PG1 = '						pages = len % 512 ? len / 512 + 1 : len / 512;\n						left = pages;\n'
PG2 = '			} else {\n				pages = len % 512 ? len / 512 + 1 : len / 512;\n'
ST1 = '				if (type > 1) {\n					s[12] = (s[12] & 0xc0) | (type & 0x3f);\n					s[9] = 32 - pages;\n'
BIGTOP = '			if (xb.bigBlock) {\n				((struct spb *)s)->b2lo'
PGT = 'pages = len % 512 ? len / 512 + 1 : len / 512;\n'
PO = [
 ('BinStop', []),
 ('BtopSt1', [(PG1, '						left = pages;\n'), (PG2, '			} else {\n'), (BIGTOP, '			if (xb.bigBlock) {\n				' + PGT + '				((struct spb *)s)->b2lo'),
              (ST1, '				if (type > 1) {\n					' + PGT + ST1.split('\n', 1)[1])]),
]
AXES = [TY, PN, PO]
