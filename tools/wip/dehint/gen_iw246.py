# attempt 17: the unused `bo = off & 0x1ffff` of build/iw/a17/s6.c (gen_iw230 big+bt+st on s4a: 6 lines, target signature, no dead test) made real: used in left, moved, x e-forms x call form x attribute.
import os
BASE = os.environ.get('IWB', 'build/iw/a17/s6.c')
DECL = '			uint32_t bo;\n\n'
BO = '				bo = off & 0x1ffff;\n'
LEFT = '						left = (off & 0x1ffff) ? 256 - (off & 0x1ffff) / 512 : 256;\n'
PG = '						pages = len % 512 ? len / 512 + 1 : len / 512;\n						left ='
TY = '				if (type > 1) {\n					((struct spt *)s)->type = type;\n					if (type != 0x2a'
S9 = 's[9] = (left - pages) >> 2;'
USE = [('un', []),
 ('u1', [(LEFT, '						left = bo ? 256 - bo / 512 : 256;\n')]),
 ('u2', [(LEFT, '						left = 256;\n						if (bo)\n							left -= bo / 512;\n')]),
 ('u3', [(LEFT, '						if (bo)\n							left = 256 - bo / 512;\n						else\n							left = 256;\n')]),
 ('u4', [(LEFT, '						left = 256 - bo / 512;\n')]),
]
PL = [('pa', []),
 ('pt', [(BO, ''), (TY, TY.replace('					if (type != 0x2a', '					bo = off & 0x1ffff;\n					if (type != 0x2a'))]),
 ('pi', [(BO, ''), (PG, '						bo = off & 0x1ffff;\n' + PG)]),
 ('ph', [(BO, ''), (DECL, DECL + '			bo = off & 0x1ffff;\n')]),
]
PGS = [('', []), ('bi', [('						pages = len % 512 ? len / 512 + 1 : len / 512;\n						left =', '						pages = len / 512;\n						if (len % 512)\n							pages++;\n						left =')])]
ES = [('', []), ('e1', [(S9, 's[9] = (left - (int)pages) >> 2;')])]
TB = [('', []), ('tb', [('	setBeU16(off >> 14, (uint8_t *)&xb.fsBlock);\n', '	setBeU16(blk, (uint8_t *)&xb.fsBlock);\n')])]
AT = [('', []), ('na', [('__attribute__((optimize("no-tree-scev-cprop"))) void writeFsTable', 'void writeFsTable')])]
AXES = [USE, PL, PGS, ES, TB, AT]
FLAGS = []
