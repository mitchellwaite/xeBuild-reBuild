# on build/iw/s2.c (pin_end and dead_add2 removed, 1 cmp left in writeFsTable's big copy): writeFsTable's own forms
BASE = 'build/iw/s2.c'
FOCUS = ['_writeFsTable']
A = '__attribute__((optimize("no-tree-scev-cprop"))) void writeFsTable'
HEAD = '''	blk = off >> 14;
	if (xb.bigBlock && (off & 0x1ffff)) {
		off = (off + 0x20000) & ~0x1ffff;
		blk = off >> 14;
	}
'''
STORE = '	fsTable[blk - xb.fsStart] = SWAP16_IMAGE_WRITE(0x1ffd);\n'
BUF = '	buf = malloc(0x4000);\n	p = buf;\n'
LOOPA = '		memcpy(p, (uint8_t *)fsTable + i * 0x200, 0x200);\n		p += 0x200;\n		memcpy(p, (uint8_t *)fsFiles + i * 0x200, 0x200);\n		p += 0x200;\n'
LOG = '	log_printf(1, "offset 0x%x len 0x4000 (end 0x%x)...", off, off + 0x4000);\n'
TAIL = '	setBeU16(blk, (uint8_t *)&xb.fsBlock);\n	setBeU16(0, (uint8_t *)&xb.fsReserved);\n	free(buf);\n'
AXES = [
 [('opt', []), ('noopt', [(A, 'void writeFsTable')])],
 [('', []),
  ('h1', [(HEAD, '	if (xb.bigBlock && (off & 0x1ffff))\n		off = (off + 0x20000) & ~0x1ffff;\n	blk = off >> 14;\n')]),
  ('h2', [(HEAD, '	if (xb.bigBlock && (off & 0x1ffff)) {\n		off = (off + 0x20000) & ~0x1ffff;\n		blk = off >> 14;\n	} else\n		blk = off >> 14;\n')]),
  ('h3', [(HEAD, '	if (xb.bigBlock) {\n		if (off & 0x1ffff) {\n			off = (off + 0x20000) & ~0x1ffff;\n		}\n	}\n	blk = off >> 14;\n')]),
  ('h4', [(HEAD, '	blk = off >> 14;\n	if (xb.bigBlock) {\n		if (off & 0x1ffff) {\n			off = (off + 0x20000) & ~0x1ffff;\n			blk = off >> 14;\n		}\n	}\n')]),
 ],
 [('', []),
  ('s1', [(STORE, '	i = blk - xb.fsStart;\n	fsTable[i] = SWAP16_IMAGE_WRITE(0x1ffd);\n')]),
  ('s2', [(STORE, '	fsTable[-xb.fsStart + blk] = SWAP16_IMAGE_WRITE(0x1ffd);\n')]),
  ('s3', [(STORE + BUF, BUF + STORE)]),
 ],
 [('', []),
  ('b1', [(BUF, '	p = buf = malloc(0x4000);\n')]),
  ('b2', [('	uint8_t *buf, *p;\n	uint32_t blk;', '	uint8_t *p;\n	uint32_t blk;\n	uint8_t *buf;'), (BUF, '	buf = malloc(0x4000);\n	p = buf;\n')]),
 ],
 [('', []),
  ('l1', [(LOOPA, '		memcpy(p, (uint8_t *)fsTable + i * 0x200, 0x200);\n		memcpy(p + 0x200, (uint8_t *)fsFiles + i * 0x200, 0x200);\n		p += 0x400;\n')]),
  ('l2', [(LOOPA, '		memcpy(p, &((uint8_t *)fsTable)[i * 0x200], 0x200);\n		p += 0x200;\n		memcpy(p, &((uint8_t *)fsFiles)[i * 0x200], 0x200);\n		p += 0x200;\n')]),
  ('l3', [(LOOPA, '		uint32_t o = i * 0x200;\n		memcpy(p, (uint8_t *)fsTable + o, 0x200);\n		p += 0x200;\n		memcpy(p, (uint8_t *)fsFiles + o, 0x200);\n		p += 0x200;\n')]),
 ],
 [('', []),
  ('g1', [(LOG, '	log_printf(1, "offset 0x%x len 0x4000 (end 0x%x)...", off, 0x4000 + off);\n')]),
 ],
 [('', []),
  ('t1', [(TAIL, '	setBeU16(blk, (uint8_t *)&xb.fsBlock);\n	setBeU16(0, (uint8_t *)&xb.fsReserved);\n	free(buf);\n	return;\n')]),
  ('t2', [(TAIL, '	setBeU16(off >> 14, (uint8_t *)&xb.fsBlock);\n	setBeU16(0, (uint8_t *)&xb.fsReserved);\n	free(buf);\n')]),
 ],
]
