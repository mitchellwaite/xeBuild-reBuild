# attempt 2, on drafts/image_write.c: subsets of the remaining dead tests (and of the merged test's conditions)
BASE = 'tools/wip/dehint/drafts/image_write.c'
A1 = '	if (x > first + 0x4000)\n		blocks += 2;\n'
A2 = '		if (x > first + 0x4000)\n			__asm__("");\n'
M = '		if (x + 0x4000 < first || (len & 0x3fff) > 0x3fff)\n			blocks++;\n'
A5 = '			if (x > first + 0x4000)\n				blocks++;\n'
A6 = '		if (x + 0x4000 < first)\n			start++;\n'
LEN = '	if ((len & 0x3fff) > 0x3fff)\n		len++;\n'
C = '		if ((len & 0x3fff) > 0x3fff)\n			abort();\n'
AXES = [
 [('', []), ('a1', [(A1, '')])],
 [('', []), ('a2', [(A2, '')])],
 [('', []),
  ('c3', [(M, '		if ((len & 0x3fff) > 0x3fff)\n			blocks++;\n')]),
  ('c4', [(M, '		if (x + 0x4000 < first)\n			blocks++;\n')]),
  ('c34', [(M, '')]),
 ],
 [('', []), ('a5', [(A5, '')])],
 [('', []), ('a6', [(A6, '')])],
 [('', []), ('len', [(LEN, '')])],
 [('', []), ('c', [(C, '')])],
]
