# attempt 8: writeFsTable without the dead test: head forms that keep a PHI on off (or a test that threads late) ahead of the inlined copies.
# Plain -O3.  Axis noopt: attribute gone too.
FLAGS = []
FOCUS = ['_writeFsTable']
BASE = 'src/image_write.c'
A = '__attribute__((optimize("no-tree-scev-cprop"))) void writeFsTable'
DD = '	if ((off & 0x3fff) > 0x3fff)\n		off += 0x4000;\n'
HEAD = '	blk = off >> 14;\n	if (xb.bigBlock && (off & 0x1ffff)) {\n		off = (off + 0x20000) & ~0x1ffff;\n		blk = off >> 14;\n	}\n'
DECL = '	uint8_t *buf, *p;\n	uint32_t blk;\n	int i;\n\n	blk = off'
DECL2 = '	uint8_t *buf, *p;\n	uint32_t blk;\n	int i, pad;\n\n	blk = off'
STORE = '	fsTable[blk - xb.fsStart] = SWAP16_IMAGE_WRITE(0x1ffd);\n'
FL = '	pad = xb.bigBlock && (off & 0x1ffff);\n'
FORMS = [
 ('dead', []),
 ('none', [(DD, '')]),
 ('f1', [(DD, ''), (DECL, DECL2), (HEAD, FL + '	if (pad)\n		off = (off + 0x20000) & ~0x1ffff;\n	blk = off >> 14;\n')]),
 ('f2', [(DD, ''), (DECL, DECL2), (HEAD, FL + '	blk = off >> 14;\n	if (pad)\n		off = (off + 0x20000) & ~0x1ffff;\n	if (pad)\n		blk = off >> 14;\n')]),
 ('f3', [(DD, ''), (DECL, DECL2), (HEAD, FL + '	if (pad)\n		off = (off + 0x20000) & ~0x1ffff;\n	blk = off >> 14;\n	if (pad)\n		blk = off >> 14;\n')]),
 ('f4', [(DD, ''), (DECL, DECL2), (HEAD, FL + '	if (pad) {\n		off = (off + 0x20000) & ~0x1ffff;\n		blk = off >> 14;\n	} else\n		blk = off >> 14;\n')]),
 ('f5', [(DD, ''), (DECL, DECL2), (HEAD, FL + '	blk = off >> 14;\n	if (pad)\n		blk = ((off + 0x20000) & ~0x1ffff) >> 14;\n	if (pad)\n		off = (off + 0x20000) & ~0x1ffff;\n')]),
 ('f6', [(DD, ''), (DECL, DECL2), (HEAD, FL + '	blk = pad ? ((off + 0x20000) & ~0x1ffff) >> 14 : off >> 14;\n	off = pad ? (off + 0x20000) & ~0x1ffff : off;\n')]),
 ('f7', [(DD, ''), (HEAD, '	if (xb.bigBlock && (off & 0x1ffff))\n		off = (off + 0x20000) & ~0x1ffff;\n	blk = off >> 14;\n')]),
 ('f8', [(DD, ''), (HEAD, '	off = xb.bigBlock && (off & 0x1ffff) ? (off + 0x20000) & ~0x1ffff : off;\n	blk = off >> 14;\n')]),
 ('f9', [(DD, ''), (HEAD, '	if (xb.bigBlock) {\n		if (off & 0x1ffff)\n			off = (off + 0x20000) & ~0x1ffff;\n		blk = off >> 14;\n	} else\n		blk = off >> 14;\n')]),
 ('f10', [(DD, ''), (DECL, DECL2), (HEAD, FL + '	if (pad)\n		off = (off + 0x20000) & ~0x1ffff;\n	blk = off >> 14;\n'), (STORE, STORE + '	if (pad)\n		blk = off >> 14;\n')]),
 ('f11', [(DD, ''), (HEAD, '	if (xb.bigBlock) {\n		uint32_t r = off & 0x1ffff;\n		if (r)\n			off += 0x20000 - r;\n	}\n	blk = off >> 14;\n')]),
 ('f12', [(DD, ''), (HEAD, '	blk = off >> 14;\n	if (xb.bigBlock) {\n		uint32_t a = (off + 0x20000) & ~0x1ffff;\n		if (off & 0x1ffff) {\n			off = a;\n			blk = a >> 14;\n		}\n	}\n')]),
 ('f13', [(DD, ''), (HEAD, '	if (xb.bigBlock && (off & 0x1ffff))\n		blk = (off = (off + 0x20000) & ~0x1ffff) >> 14;\n	else\n		blk = off >> 14;\n')]),
 ('f14', [(DD, ''), (HEAD, '	blk = off >> 14;\n	if (xb.bigBlock && (off & 0x1ffff))\n		blk = (off = (off + 0x20000) & ~0x1ffff) >> 14;\n')]),
]
AXES = [
 [('', []), ('noopt', [(A, 'void writeFsTable')])],
 FORMS,
]
