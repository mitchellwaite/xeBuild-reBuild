# attempt 6: the off-only statement in the loop without touching BLK * 32: s[9]'s (off & 0x1ffff) part computed up front like `pages`
import os


S9 = '						s[9] = (((off & 0x1ffff) ? 256 - (off & 0x1ffff) / 512 : 256) - left) >> 2;\n'
PAGES = '			pages = len % 512 ? len / 512 + 1 : len / 512;\n'
OUT = '	for (b = 0; b < blocks; b++) {\n'
INNER = '		for (end = p + npages; p < end; p++) {\n'
PART = "		partial = (len < 0x4000) & (type != 0) & (type != '0');\n"
USE = ('						s[9] = (pg - left) >> 2;\n')
A = "(off & 0x1ffff) ? 256 - (off & 0x1ffff) / 512 : 256"
AV = '''if (off & 0x1ffff)
				pg = 256 - (off & 0x1ffff) / 512;
			else
				pg = 256;
'''
AXES = [
 [('ip', [(PAGES, '			pg = %s;\n' % A + PAGES), (S9, USE)]),
  ('ia', [(PAGES, PAGES + '			pg = %s;\n' % A), (S9, USE)]),
  ('iv', [(PAGES, '			' + AV + PAGES), (S9, USE)]),
  ('o', [(OUT, OUT + '		pg = %s;\n' % A), (S9, USE)]),
  ('b', [(INNER, '		pg = %s;\n' % A + INNER), (S9, USE)]),
  ('m', [('			memset(s, 0, 16);\n			if (xb.bigBlock) {\n				((struct spb', '			memset(s, 0, 16);\n			pg = %s;\n			if (xb.bigBlock) {\n				((struct spb' % A), (S9, USE)]),
  ('pgk', [])],
 [('', []),
  ('pb', [(PART, "		partial = type != 0 && type != '0' && len < 0x4000;\n")]),
  ('pa', [(PART, "		partial = len < 0x4000 && type != 0 && type != '0';\n")])],
 [('', []), ('t0', [('		tail = rem;\n		if (rem >= 0x4000)\n			tail = rem % 0x4000;\n', '''		if (rem < 0x4000)
			tail = rem;
		else
			tail = rem % 0x4000;
''')])],
]
BASE = 'build/iw/a6/r1.c'
FLAGS = []
