# attempt 8: from n7 (no hot label): constprop.1's page-loop compare wants the split-paths copy's name below 82.  Named locals and spellings in imgAdd.
import os
FLAGS = []
BASE = os.environ.get('IWB', 'build/iw/a8/n7.c')
FOCUS = ['_imgAdd', '_imgAdd.constprop.1', '_imgAdd.constprop.2', '_imgAdd.constprop.4', '_imgAddFile', '_writeInitialHeader']
BL = '		blk = start + b;\n'
U1 = '				((struct spb *)s)->b2lo = blk >> 8;\n'
PGS = '			pg = start * 32;\n			s = xb.spare + (pg + p + b * 32) * 16;\n'
TL = '		tail = rem;\n		if (rem >= 0x4000)\n			tail = rem % 0x4000;\n'
F = '	for (b = 0; b < blocks; b++) {\n'
E = '		for (end = p + npages; p < end; p++) {\n'
T = "		t = type - '1';\n"
PA = "		partial = (len < 0x4000) & (type != 0) & (type != '0');\n"
A1 = [
 ('', []),
 ('b0', [(BL, ''), (U1, '				((struct spb *)s)->b2lo = BLK >> 8;\n')]),
 ('b1', [(U1, '				((struct spb *)s)->b2lo = BLK >> 8;\n'), ('				s[1] = BLK;\n', '				s[1] = blk;\n')]),
 ('b2', [('				((struct sps *)s)->b1lo = BLK >> 8;\n', '				((struct sps *)s)->b1lo = blk >> 8;\n')]),
 ('b3', [('				s[0] = BLK;\n', '				s[0] = blk;\n')]),
 ('b4', [('				s[1] = BLK;\n', '				s[1] = blk;\n')]),
 ('b5', [('				s[1] = BLK;\n', '				s[1] = blk;\n'), ('				s[0] = BLK;\n', '				s[0] = blk;\n')]),
 ('b6', [('				s[1] = BLK;\n', '				s[1] = blk;\n'), ('				s[0] = BLK;\n', '				s[0] = blk;\n'), ('				((struct sps *)s)->b1lo = BLK >> 8;\n', '				((struct sps *)s)->b1lo = blk >> 8;\n')]),
]
A2 = [
 ('', []),
 ('t1', [(TL, '		tail = rem < 0x4000 ? rem : rem % 0x4000;\n')]),
 ('t2', [(TL, '		tail = rem % 0x4000;\n')]),
]
A3 = [
 ('', []),
 ('e1', [(E, '		end = p + npages;\n		for (; p < end; p++) {\n')]),
 ('e2', [(E, '		for (end = npages + p; p < end; p++) {\n')]),
 ('e3', [(E, '		for (end = p + npages; end > p; p++) {\n')]),
 ('e4', [(E, '		for (end = p + npages; p != end; p++) {\n')]),
]
A4 = [
 ('', []),
 ('q1', [(PA, "		partial = (type != 0) & (type != '0') & (len < 0x4000);\n")]),
 ('q2', [(PA, "		partial = (len < 0x4000) & ((type != 0) & (type != '0'));\n")]),
 ('q3', [(PA + T, T + PA)]),
]
AXES = [A1, A2, A3, A4]
