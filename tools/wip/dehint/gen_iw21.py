# attempt 2, on drafts/image_write.c: c1's cold label -> noreturn call; gimple then equals the draft's but for one SSA
# version (npages_128 vs npages_214 in the big copy).  Forms of imgAddFile's preamble and dead tests to get it back.
BASE = 'tools/wip/dehint/drafts/image_write.c'
C = '''		if ((len & 0x3fff) > 0x3fff) {
			c1: __attribute__((cold));
			name++;
		}
'''
LEN = '	if (end < off && (len & 0x3fff) > 0x3fff)\n		len++;\n'
LIM = '''	uint32_t lim = (xb.fsEnd - 1) * 0x4000;
	uint32_t end = off + len;
'''
TEST = '	if (__builtin_expect(lim >= off + len, 1)) {\n'
AXES = [
 [('ab', [(C, '		if ((len & 0x3fff) > 0x3fff)\n			abort();\n')]),
  ('ex', [(C, '		if ((len & 0x3fff) > 0x3fff)\n			exit(1);\n')]),
  ('ab2', [(C, '		if ((len & 0x3fff) >= 0x4000)\n			abort();\n')]),
  ('ab3', [(C, '		if (len > 0x3fff && (len & 0x3fff) > 0x3fff)\n			abort();\n')]),
  ('ab4', [(C, '		if (end < off || (len & 0x3fff) > 0x3fff)\n			abort();\n')]),
  ('ab5', [(C, '		if ((len & 0x3fff) > 0x3fff || end < off)\n			abort();\n')]),
  ('ab6', [(C, '		if (end < off && (len & 0x3fff) > 0x3fff)\n			abort();\n')]),
  ('ab7', [(C, '		if ((end & 0x3fff) > 0x3fff)\n			abort();\n')]),
  ('ab8', [(C, '		if (lim < end && (len & 0x3fff) > 0x3fff)\n			abort();\n')]),
  ('ab9', [(C, '		if (end > lim)\n			abort();\n')]),
 ],
 [('', []),
  ('l1', [(LEN, '	if (end < off && (len & 0x3fff) > 0x3fff)\n		len += 1;\n')]),
  ('l2', [(LEN, '	if ((len & 0x3fff) > 0x3fff && end < off)\n		len++;\n')]),
  ('l3', [(LEN, '	if (end < off && (len & 0x3fff) > 0x3fff)\n		len += 2;\n')]),
  ('l4', [(LEN, '	if (end < off) if ((len & 0x3fff) > 0x3fff)\n		len++;\n')]),
  ('l5', [(LEN, '	if (end < len && (len & 0x3fff) > 0x3fff)\n		len++;\n')]),
  ('l6', [(LEN, '	if (end < off && (len & 0x3fff) > 0x3fff)\n		off++;\n')]),
 ],
 [('', []),
  ('o1', [(LIM, '	uint32_t end = off + len;\n	uint32_t lim = (xb.fsEnd - 1) * 0x4000;\n')]),
  ('o2', [(LIM, '	uint32_t lim = xb.fsEnd * 0x4000 - 0x4000;\n	uint32_t end = off + len;\n')]),
  ('o3', [(LIM, '	uint32_t lim = (xb.fsEnd - 1) << 14;\n	uint32_t end = off + len;\n')]),
 ],
 [('', []),
  ('t1', [(TEST, '	if (__builtin_expect(off + len <= lim, 1)) {\n')]),
 ],
]
