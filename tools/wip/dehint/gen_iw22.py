# attempt 2, on drafts/image_write.c (c1 is a noreturn test on end): imgAddFile's preamble without its other tricks.
BASE = 'tools/wip/dehint/drafts/image_write.c'
C = '		if ((end & 0x3fff) > 0x3fff)\n			abort();\n'
LEN = '	if (end < off && (len & 0x3fff) > 0x3fff)\n		len++;\n'
LIM = '''	uint32_t lim = (xb.fsEnd - 1) * 0x4000;
	uint32_t end = off + len;
'''
TEST = '	if (__builtin_expect(lim >= off + len, 1)) {\n'
AXES = [
 [('', []),
  ('L0', [(LEN, '')]),
  ('Lp', [(LEN, '	if ((len & 0x3fff) > 0x3fff)\n		len++;\n')]),
  ('Le', [(LEN, '	if ((end & 0x3fff) > 0x3fff)\n		len++;\n')]),
  ('La', [(LEN, '	if ((len & 0x3fff) > 0x3fff)\n		abort();\n')]),
  ('Lb', [(LEN, '	if ((end & 0x3fff) > 0x3fff)\n		abort();\n')]),
 ],
 [('', []),
  ('C0', [(C, '')]),
  ('Cl', [(C, '		if ((len & 0x3fff) > 0x3fff)\n			abort();\n')]),
  ('Cn', [(C, '		if ((end & 0x3fff) > 0x3fff) {\n			name++;\n			abort();\n		}\n')]),
 ],
 [('', []),
  ('nx', [(TEST, '	if (lim >= off + len) {\n')]),
  ('nxe', [(TEST, '	if (lim >= end) {\n')]),
  ('xe', [(TEST, '	if (__builtin_expect(lim >= end, 1)) {\n')]),
 ],
 [('', []),
  ('o1', [(LIM, '	uint32_t end = off + len;\n	uint32_t lim = (xb.fsEnd - 1) * 0x4000;\n')]),
 ],
]
