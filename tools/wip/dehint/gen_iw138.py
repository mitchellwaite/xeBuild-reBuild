# attempt 8: pages position per arm (gen_iw136) x npages' predicted forms (gen_iw134) x t (`unsigned t`, uint8_t, uint8_t with pin).  Base n2.
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
]
N = '''		if (partial) {
			if (len % 512)
				npages = (len + 512) / 512;
			else
				npages = len / 512;
		} else
			npages = 32;
'''
C = '''			if (len % 512)
				npages = (len + 512) / 512;
			else
				npages = len / 512;
'''
NF = [('n1', N),
 ('n3', '		if (partial > 0) {\n' + C + '		} else\n			npages = 32;\n'),
 ('n2', '		if (partial <= 0)\n			npages = 32;\n		else {\n' + C + '		}\n'),
 ('n7', '''		if (len % 512)
			npages = (len + 512) / 512;
		else
			npages = len / 512;
		if (partial <= 0)
			npages = 32;
'''),
]
TD = '	unsigned t;\n'
TC = 'if ((uint8_t)t < 15) {'
A = '			p = xb.bigBlock ? off & 0x1ffff : off & 0x3fff;\n'
TF = [('ti', []), ('tb', [(TD, '	uint8_t t;\n'), (TC, 'if (t < 15) {')]),
      ('tp', [(TD, '	uint8_t t;\n'), (TC, 'if (t < 15) {'), (A, '			__asm__("" :: "g"(t));\n' + A)])]
AXES = [[('', [(COM, '')])], BF, SF, [(a, [(N, b)]) for a, b in NF], TF]
