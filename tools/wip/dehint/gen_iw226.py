# attempt 15: `small` two-step partial (gen_iw225's best, 12 lines) x block offset placement x test x tail spelling.
import os
BASE = os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_a14.c')
P0 = "		partial = (len < 0x4000) & (type != 0) & (type != '0');\n"
DECL = '	int partial;\n'
SM = [
 ('s2', [(P0, "		small = type != 0 && type != '0';\n		partial = small && len < 0x4000;\n"), (DECL, DECL + '	_Bool small;\n')]),
 ('s2i', [(P0, "		small = type != 0 && type != '0';\n		partial = small && len < 0x4000;\n"), (DECL, DECL + '	int small;\n')]),
 ('s3', [(P0, "		small = type != 0 && type != '0';\n		partial = len < 0x4000 && small;\n"), (DECL, DECL + '	_Bool small;\n')]),
 ('s4', [(P0, "		small = 0;\n		if (type != 0 && type != '0')\n			small = 1;\n		partial = small && len < 0x4000;\n"), (DECL, DECL + '	_Bool small;\n')]),
 ('s5', [(P0, "		small = type != 0 && type != '0';\n		partial = small & (len < 0x4000);\n"), (DECL, DECL + '	_Bool small;\n')]),
 ('s6', [(P0, "		small = (type != 0) & (type != '0');\n		partial = small && len < 0x4000;\n"), (DECL, DECL + '	_Bool small;\n')]),
 ('s7', [(P0, "		small = type != 0 && type != '0';\n		partial = small ? len < 0x4000 : 0;\n"), (DECL, DECL + '	_Bool small;\n')]),
]
T = [('', []), ('t1', [('		if (partial > 0) {\n', '		if (partial) {\n')])]
S9 = '						s[9] = (((off & 0x1ffff) ? 256 - (off & 0x1ffff) / 512 : 256) - left) >> 2;\n'
USE = '						s[9] = ((bo ? 256 - bo / 512 : 256) - left) >> 2;\n'
D = 'uint32_t bo = off & 0x1ffff;\n'
BO = [('', []),
 ('bL', [('			/* a statement of its own: computed from params alone', '			' + D + '\n			/* a statement of its own: computed from params alone'), (S9, USE)]),
 ('bA', [('					if (type != 0x2a && type != 0x2c) {\n', '					if (type != 0x2a && type != 0x2c) {\n						' + D), (S9, USE)]),
 ('bU', [(S9, '						' + D + USE)]),
]
TL = [('', []), ('tb', [('	setBeU16(off >> 14, (uint8_t *)&xb.fsBlock);\n', '	setBeU16(blk, (uint8_t *)&xb.fsBlock);\n')])]
AXES = [SM, T, BO, TL]
FLAGS = []
