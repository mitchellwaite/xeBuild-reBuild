# attempt 16: after the first IDENTICAL state (L3re1+ba+st+g+to in gen_iw235): which borderline shapes it can lose, and whether the dead test can go. Base build/iw/a16/m0.c, saved in the notes as drafts/image_write_a16.c.
import os
BASE = os.environ.get('IWB', 'build/iw/a16/m0.c')
P0 = "		partial = (len < 0x4000) & (type != 0) & (type != '0');\n"
DEAD = '	if ((off & 0x3fff) > 0x3fff)\n		off += 0x4000;\n'
B0 = '''						pages = len / 512;
						if (len % 512)
							pages++;
'''
S0 = '				pages = len % 512 ? len / 512 + 1 : len / 512;\n'
PF = [('', []),
      ('sm', [(P0, "		small = type != 0 && type != '0';\n		partial = small && len < 0x4000;\n"), ('	int partial;\n', '	int partial;\n	_Bool small;\n')]),
      ('sm2', [(P0, "		small = 0;\n		if (type != 0 && type != '0')\n			small = 1;\n		partial = small && len < 0x4000;\n"), ('	int partial;\n', '	int partial;\n	_Bool small;\n')]),
      ]
T = [('', []), ('t1', [('		if (partial > 0) {\n', '		if (partial) {\n')])]
DT = [('', []), ('nd', [(DEAD, '')])]
PG = [('', []),
      ('si', [(S0, '				if (len % 512)\n					pages = len / 512 + 1;\n				else\n					pages = len / 512;\n')]),
      ('sa', [(S0, '				pages = len / 512;\n				if (len % 512)\n					pages++;\n')]),
      ('bt', [(B0, '						pages = len % 512 ? len / 512 + 1 : len / 512;\n')]),
      ]
TL = [('', []), ('tb', [('	setBeU16(off >> 14, (uint8_t *)&xb.fsBlock);\n', '	setBeU16(blk, (uint8_t *)&xb.fsBlock);\n')])]
AXES = [PF, T, DT, PG, TL]
FLAGS = []
