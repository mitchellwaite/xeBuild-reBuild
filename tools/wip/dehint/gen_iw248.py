# attempt 17: on build/iw/a17/s2c.c (2 lines, constprop.1's compare; t computed after p = 0): bi made constprop.1 clean on s4t, so bo's place x bi x e-form x left x small pages x tail x t's place.
import os
BASE = os.environ.get('IWB', 'build/iw/a17/s2c.c')
BO = '					bo = off & 0x1ffff;\n'
TY = '				if (type > 1) {\n					((struct spt *)s)->type = type;\n					bo = off & 0x1ffff;\n'
PG = '						pages = len % 512 ? len / 512 + 1 : len / 512;\n						left ='
LEFT = '						left = bo ? 256 - bo / 512 : 256;\n'
S9 = 's[9] = (left - pages) >> 2;'
AXES = [
 [('', []), ('bi', [(PG, '						pages = len / 512;\n						if (len % 512)\n							pages++;\n						left =')]),
  ('be', [(PG, '						if (len % 512)\n							pages = len / 512 + 1;\n						else\n							pages = len / 512;\n						left =')])],
 [('', []),
  ('pa', [(BO, ''), ('				((struct spb *)s)->b2lo', '				bo = off & 0x1ffff;\n				((struct spb *)s)->b2lo')]),
  ('pi', [(BO, ''), ('					if (type != 0x2a && type != 0x2c) {\n', '					if (type != 0x2a && type != 0x2c) {\n						bo = off & 0x1ffff;\n')]),
  ('pl', [(BO, ''), (LEFT, '						bo = off & 0x1ffff;\n' + LEFT)]),
 ],
 [('', []), ('l2', [(LEFT, '						left = 256;\n						if (bo)\n							left -= bo / 512;\n')]), ('l3', [(LEFT, '						if (bo)\n							left = 256 - bo / 512;\n						else\n							left = 256;\n')])],
 [('', []), ('e1', [(S9, 's[9] = (left - (int)pages) >> 2;')]), ('e4', [(S9, 's[9] = (left - pages) >> 2 & 0xff;')]), ('e6', [('	int left;\n', '	uint32_t left;\n'), (S9, 's[9] = (int)(left - pages) >> 2;')])],
 [('', []), ('tb', [('	setBeU16(off >> 14, (uint8_t *)&xb.fsBlock);\n', '	setBeU16(blk, (uint8_t *)&xb.fsBlock);\n')])],
]
FLAGS = []
