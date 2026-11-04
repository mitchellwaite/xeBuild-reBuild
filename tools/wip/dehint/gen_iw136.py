# attempt 8: n2 (imgAdd and clones right, writeInitialHeader's call over the inline limit by 0.17%): where pages is computed, per arm.
import os
FLAGS = []
BASE = os.environ.get('IWB', 'build/iw/a8/n2.c')
FOCUS = ['_imgAdd', '_imgAdd.constprop.1', '_imgAdd.constprop.2', '_imgAdd.constprop.4', '_imgAddFile', '_writeInitialHeader']
COM = '''			/* pages here and left in the big arm: lim2 then hoists left
			   after len >> 8 and the type tests, as in the original */
			pages = len % 512 ? len / 512 + 1 : len / 512;
'''
PG = 'pages = len % 512 ? len / 512 + 1 : len / 512;\n'
BIGTOP = '			if (xb.bigBlock) {\n				((struct spb *)s)->b2lo'
SMTOP = '			} else {\n				((struct sps *)s)->b1lo'
BT1 = '				if (type > 1) {\n					s[12] = (s[12] & 0xc0) | (type & 0x3f);\n					if (type != 0x2a && type != 0x2c) {\n'
BIN = BT1 + '						left = pages;\n'
ST1 = '				if (type > 1) {\n					s[12] = (s[12] & 0xc0) | (type & 0x3f);\n					s[9] = 32 - pages;\n'
BF = [
 ('Btop', [(BIGTOP, '			if (xb.bigBlock) {\n				' + PG + '				((struct spb *)s)->b2lo')]),
 ('Bt1', [(BT1, '				if (type > 1) {\n					' + PG + BT1.split('\n', 1)[1])]),
 ('Bin', [(BIN, BT1 + '						' + PG + '						left = pages;\n')]),
]
SF = [
 ('Stop', [(SMTOP, '			} else {\n				' + PG + '				((struct sps *)s)->b1lo')]),
 ('St1', [(ST1, '				if (type > 1) {\n					' + PG + ST1.split('\n', 1)[1])]),
 ('Sin', [(ST1, '				if (type > 1) {\n					s[12] = (s[12] & 0xc0) | (type & 0x3f);\n					' + PG + '					s[9] = 32 - pages;\n')]),
]
AXES = [[('', [(COM, '')])], BF, SF]
