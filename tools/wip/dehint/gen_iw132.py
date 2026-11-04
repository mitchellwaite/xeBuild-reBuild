# attempt 8: n2: writeInitialHeader's inlined call is imgAdd(0, &hdrTemplate, sizeof, 0, 0x1ffb, 1): len known, the saving is the "(op2 changed)" statements in the loops.
# Move pages (hot, derived from len only) out of the inner loop.
import os
FLAGS = []
BASE = os.environ.get('IWB', 'build/iw/a8/n2.c')
FOCUS = ['_imgAdd', '_imgAdd.constprop.1', '_imgAdd.constprop.2', '_imgAdd.constprop.4', '_imgAddFile', '_writeInitialHeader']
COM = '''			/* pages here and left in the big arm: lim2 then hoists left
			   after len >> 8 and the type tests, as in the original */
			pages = len % 512 ? len / 512 + 1 : len / 512;
'''
FP = '		for (end = p + npages; p < end; p++) {\n'
OL = '	for (b = 0; b < blocks; b++) {\n'
ST = '			if (type > 1) {\n'
E1 = '		pages = len % 512 ? len / 512 + 1 : len / 512;\n'
AXES = [[
 ('base', []),
 ('outer', [(COM, ''), (FP, E1 + FP)]),
 ('outer2', [(COM, ''), (OL, OL + E1)]),
 ('head', [(COM, ''), ('#define BLK (start + b)\n', '	pages = len % 512 ? len / 512 + 1 : len / 512;\n#define BLK (start + b)\n')]),
 ('t0', [('		if (partial) {\n			if (len % 512)\n				npages = (len + 512) / 512;\n			else\n				npages = len / 512;\n		} else\n			npages = 32;\n',
          '		pages = len % 512 ? len / 512 + 1 : len / 512;\n		npages = partial ? pages : 32;\n'), (COM, '')]),
 ('t1', [('		if (partial) {\n			if (len % 512)\n				npages = (len + 512) / 512;\n			else\n				npages = len / 512;\n		} else\n			npages = 32;\n',
          '		pages = len % 512 ? len / 512 + 1 : len / 512;\n		npages = 32;\n		if (partial)\n			npages = pages;\n'), (COM, '')]),
 ('arm', [(COM, ''), ('				if (type > 1) {\n					s[12] = (s[12] & 0xc0) | (type & 0x3f);\n					if (type != 0x2a', '				if (type > 1) {\n					pages = len % 512 ? len / 512 + 1 : len / 512;\n					s[12] = (s[12] & 0xc0) | (type & 0x3f);\n					if (type != 0x2a'),
          ('					s[12] = (s[12] & 0xc0) | (type & 0x3f);\n					s[9] = 32 - pages;', '					s[12] = (s[12] & 0xc0) | (type & 0x3f);\n					pages = len % 512 ? len / 512 + 1 : len / 512;\n					s[9] = 32 - pages;')]),
]]
