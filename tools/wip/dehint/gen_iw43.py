# attempt 3: near removal sets from gen_iw42 crossed with writeFsTable's forms.
M = '		if (x + 0x4000 < first || (len & 0x3fff) > 0x3fff)\n			blocks++;\n'
A1 = '	if (x > first + 0x4000)\n		blocks += 2;\n'
A2 = '		if (x > first + 0x4000)\n			__asm__("");\n'
A6 = '		if (x + 0x4000 < first)\n			start++;\n'
T = "		t = type - '1';\n		partial = type != 0 && type != '0' && len < 0x4000;\n"
LIM = '	uint32_t lim = (xb.fsEnd - 1) * 0x4000;\n'
L = '	if ((len & 0x3fff) > 0x3fff)\n		len++;\n'
a1 = (A1, '')
c3 = (M, '		if ((len & 0x3fff) > 0x3fff)\n			blocks++;\n')
ab2 = (A2, '		if (x > first + 0x4000)\n			blocks += 2;\n')
ab1 = (A2, '		if (x > first + 0x4000)\n			blocks++;\n')
abs_ = (A2, '		if (x > first + 0x4000)\n			start++;\n')
a0 = (A2, '')
t = (T, "		partial = type != 0 && type != '0' && len < 0x4000;\n		t = type - '1';\n")
e = [(LIM, LIM + '	uint32_t end = off + len;\n'), (L, '	if (end < off && (len & 0x3fff) > 0x3fff)\n		len++;\n')]
s1 = (A6, '		if (x + 0x4000 < first)\n			blocks++;\n')
SETS = [
 ('A0te', [a0, t] + e),
 ('A1b2te', [a1, ab2, t] + e),
 ('A1b1te', [a1, ab1, t] + e),
 ('A1C3Ase', [a1, c3, abs_, s1] + e),
 ('A1A0tes1', [a1, a0, t, s1] + e),
 ('A1C3b2te', [a1, c3, ab2, t] + e),
 ('A1C3b2tes1', [a1, c3, ab2, t, s1] + e),
 ('A1b2tes1', [a1, ab2, t, s1] + e),
 ('C3b2te', [c3, ab2, t] + e),
 ('C3b1te', [c3, ab1, t] + e),
]
HEAD = '	blk = off >> 14;\n	if (xb.bigBlock && (off & 0x1ffff)) {\n		off = (off + 0x20000) & ~0x1ffff;\n		blk = off >> 14;\n	}\n'
STORE = '	fsTable[blk - xb.fsStart] = SWAP16_IMAGE_WRITE(0x1ffd);\n'
BUF = '	buf = malloc(0x4000);\n	p = buf;\n'
TL = '	setBeU16(blk, (uint8_t *)&xb.fsBlock);\n'
AXES = [
 SETS,
 [('', []),
  ('h1', [(HEAD, '	if (xb.bigBlock && (off & 0x1ffff))\n		off = (off + 0x20000) & ~0x1ffff;\n	blk = off >> 14;\n')]),
  ('h2', [(HEAD, '	if (xb.bigBlock && (off & 0x1ffff)) {\n		off = (off + 0x20000) & ~0x1ffff;\n		blk = off >> 14;\n	} else\n		blk = off >> 14;\n')]),
  ('h4', [(HEAD, '	blk = off >> 14;\n	if (xb.bigBlock) {\n		if (off & 0x1ffff) {\n			off = (off + 0x20000) & ~0x1ffff;\n			blk = off >> 14;\n		}\n	}\n')]),
 ],
 [('', []),
  ('s1', [(STORE, '	i = blk - xb.fsStart;\n	fsTable[i] = SWAP16_IMAGE_WRITE(0x1ffd);\n')]),
  ('s2', [(STORE, '	fsTable[-xb.fsStart + blk] = SWAP16_IMAGE_WRITE(0x1ffd);\n')]),
  ('s3', [(STORE + BUF, BUF + STORE)]),
 ],
 [('', []), ('t2', [(TL, '	setBeU16(off >> 14, (uint8_t *)&xb.fsBlock);\n')])],
]
