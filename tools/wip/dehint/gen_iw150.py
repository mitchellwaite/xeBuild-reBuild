# attempt 8: from n7, with the pin: where t is computed (initial SSA versions follow statement order) x t's type x pages place and spelling.
import os
FLAGS = []
BASE = os.environ.get('IWB', 'build/iw/a8/n7.c')
FOCUS = ['_imgAdd', '_imgAdd.constprop.1', '_imgAdd.constprop.2', '_imgAdd.constprop.4', '_imgAddFile', '_writeInitialHeader']
TL = "		t = type - '1';\n"
BL = '		blk = start + b;\n'
PA = "		partial = (len < 0x4000) & (type != 0) & (type != '0');\n"
NP = '		if (partial > 0) {\n'
P0 = '		p = 0;\n'
OL = '	for (b = 0; b < blocks; b++) {\n'
TQ = "	t = type - '1';\n"
MC = '#define BLK (start + b)\n'
TP = [
 ('', []),
 ('a', [(PA + TL, PA), (BL, TL + BL)]),
 ('b', [(PA + TL, TL + PA)]),
 ('c', [(TL, ''), (P0, TL + P0)]),
 ('d', [(TL, ''), (NP, TL + NP)]),
 ('e', [(TL, ''), (OL, TQ + OL)]),
 ('f', [(TL, ''), ('		if (t < 15) {\n', "		t = type - '1';\n		if (t < 15) {\n")]),
]
D = '	uint8_t t;\n'
C = 'if (t < 15) {'
TY = [('u8', []), ('ch', [(D, '	char t;\n'), (C, 'if ((uint8_t)t < 15) {')]), ('sc', [(D, '	signed char t;\n'), (C, 'if ((uint8_t)t < 15) {')])]
B0 = '						pages = len % 512 ? len / 512 + 1 : len / 512;\n						left = pages;\n'
S0 = '			} else {\n				pages = len % 512 ? len / 512 + 1 : len / 512;\n				((struct sps *)s)->b1lo = BLK >> 8;\n'
ST1 = '				if (type > 1) {\n					s[12] = (s[12] & 0xc0) | (type & 0x3f);\n					s[9] = 32 - pages;\n'
BIGTOP = '			if (xb.bigBlock) {\n				((struct spb *)s)->b2lo'
PGT = 'pages = len % 512 ? len / 512 + 1 : len / 512;\n'
PO = [
 ('BinStop', []),
 ('BiStop', [(B0, '						pages = len / 512;\n						if (len % 512)\n							pages++;\n						left = pages;\n')]),
 ('BtopSt1', [(B0, '						left = pages;\n'), (S0, '			} else {\n				((struct sps *)s)->b1lo = BLK >> 8;\n'), (BIGTOP, '			if (xb.bigBlock) {\n				' + PGT + '				((struct spb *)s)->b2lo'),
              (ST1, '				if (type > 1) {\n					' + PGT + ST1.split('\n', 1)[1])]),
]
AXES = [TP, TY, PO]
