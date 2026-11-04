# attempt 8: from n5 (`if (partial > 0)`, pages in the arms, pin_t kept): which local forms move the three compares (constprop.1, constprop.4, imgAddFile)?
import os
FLAGS = []
BASE = os.environ.get('IWB', 'build/iw/a8/n5.c')
FOCUS = ['_imgAdd', '_imgAdd.constprop.1', '_imgAdd.constprop.2', '_imgAdd.constprop.4', '_imgAddFile']
L1 = '						pages = len % 512 ? len / 512 + 1 : len / 512;\n						left = pages;\n'
LF = [
 ('', []),
 ('l2', [(L1, '						left = len % 512 ? len / 512 + 1 : len / 512;\n')]),
 ('l3', [(L1, '						left = len / 512;\n						if (len % 512)\n							left++;\n')]),
 ('l4', [(L1, '						pages = len / 512;\n						if (len % 512)\n							pages++;\n						left = pages;\n')]),
]
S0 = '					pages = len % 512 ? len / 512 + 1 : len / 512;\n					s[9] = 32 - pages;\n'
SF = [
 ('', []),
 ('s1', [(S0, '					s[9] = 32 - (len % 512 ? len / 512 + 1 : len / 512);\n')]),
 ('s3', [(S0, '					pages = len / 512;\n					if (len % 512)\n						pages++;\n					s[9] = 32 - pages;\n')]),
]
C = '''			if (len % 512)
				npages = (len + 512) / 512;
			else
				npages = len / 512;
'''
CF = [
 ('', []),
 ('c1', [(C, '			npages = len / 512;\n			if (len % 512)\n				npages++;\n')]),
 ('c2', [(C, '			npages = len % 512 ? (len + 512) / 512 : len / 512;\n')]),
 ('c3', [(C, '			npages = len % 512 ? len / 512 + 1 : len / 512;\n')]),
 ('c4', [(C, '			if (len % 512)\n				npages = len / 512 + 1;\n			else\n				npages = len / 512;\n')]),
]
BL = '		blk = start + b;\n'
PA = "		partial = (len < 0x4000) & (type != 0) & (type != '0');\n"
TF = [
 ('', []),
 ('b0', [(BL, ''), ('				((struct spb *)s)->b2lo = blk >> 8;\n', '				((struct spb *)s)->b2lo = BLK >> 8;\n')]),
 ('t1', [(PA + "		t = type - '1';\n", "		t = type - '1';\n" + PA)]),
 ('pu', [('	int partial;\n', '	uint8_t partial;\n')]),
]
AXES = [LF, SF, CF, TF]
