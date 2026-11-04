# attempt 17: writeFsTable-only forms on build/iw/a17/n8.c (imgAdd and clones clean, plain -O3, 3 tricks if writeFsTable lands): head forms, loop forms, tail, length, and small statements that move names without a dead test.
import os
BASE = os.environ.get('IWB', 'build/iw/a17/n8.c')
HEAD = '	blk = off >> 14;\n	if (xb.bigBlock && (off & 0x1ffff)) {\n		off = (off + 0x20000) & ~0x1ffff;\n		blk = off >> 14;\n	}\n'
TAB = '	fsTable[blk - xb.fsStart] = SWAP16_IMAGE_WRITE(0x1ffd);\n'
LOOP = '''	buf = malloc(0x4000);
	p = buf;
	for (i = 0; i < 16; i++) {
		memcpy(p, (uint8_t *)fsTable + i * 0x200, 0x200);
		p += 0x200;
		memcpy(p, (uint8_t *)fsFiles + i * 0x200, 0x200);
		p += 0x200;
	}
'''
TAIL = '	setBeU16(off >> 14, (uint8_t *)&xb.fsBlock);\n'
H = [('', []),
 ('h1', [(HEAD, '	if (xb.bigBlock && (off & 0x1ffff))\n		off = (off + 0x20000) & ~0x1ffff;\n	blk = off >> 14;\n')]),
 ('h2', [(HEAD, '	if (xb.bigBlock) {\n		if (off & 0x1ffff)\n			off = (off + 0x20000) & ~0x1ffff;\n	}\n	blk = off >> 14;\n')]),
 ('h3', [(HEAD, '	if (xb.bigBlock && (off & 0x1ffff)) {\n		off = (off + 0x20000) & ~0x1ffff;\n	}\n	blk = off / 0x4000;\n')]),
 ('h4', [(HEAD, '	blk = off >> 14;\n	if (xb.bigBlock && (off & 0x1ffff)) {\n		blk = (off + 0x20000) >> 14 & ~7;\n		off = blk << 14;\n	}\n')]),
 ('h5', [(HEAD, '	blk = off >> 14;\n	if (xb.bigBlock && (off & 0x1ffff)) {\n		off = (off + 0x20000) & ~0x1ffff;\n		blk = off / 0x4000;\n	}\n')]),
]
L = [('', []),
 ('l1', [(LOOP, LOOP.replace('p += 0x200;\n		memcpy(p, (uint8_t *)fsFiles', 'memcpy(p + 0x200, (uint8_t *)fsFiles').replace('p += 0x200;', 'p += 0x400;'))]),
 ('l2', [(LOOP, LOOP.replace('p = buf;\n	for (i = 0; i < 16; i++) {', 'for (p = buf, i = 0; i < 16; i++) {'))]),
 ('l3', [(LOOP, LOOP.replace('(uint8_t *)fsTable + i * 0x200', '&((uint8_t *)fsTable)[i * 0x200]').replace('(uint8_t *)fsFiles + i * 0x200', '&((uint8_t *)fsFiles)[i * 0x200]'))]),
 ('l4', [(LOOP, LOOP.replace('p = buf;\n', '').replace('memcpy(p, (uint8_t *)fsTable', 'p = buf + i * 0x400;\n		memcpy(p, (uint8_t *)fsTable').replace('		memcpy(p, (uint8_t *)fsFiles + i * 0x200, 0x200);\n		p += 0x200;\n', '		memcpy(p, (uint8_t *)fsFiles + i * 0x200, 0x200);\n'))]),
]
T = [('', []),
 ('tb', [(TAIL, '	setBeU16(blk, (uint8_t *)&xb.fsBlock);\n')]),
 ('t2', [(TAIL, '	setBeU16(off / 0x4000, (uint8_t *)&xb.fsBlock);\n')]),
 ('t3', [(TAIL, '	blk = off >> 14;\n	setBeU16(blk, (uint8_t *)&xb.fsBlock);\n')]),
]
C = [('', []), ('ck', [(TAB, '	fsTable[-xb.fsStart + blk] = SWAP16_IMAGE_WRITE(0x1ffd);\n')]), ('ci', [(TAB, '	i = blk - xb.fsStart;\n	fsTable[i] = SWAP16_IMAGE_WRITE(0x1ffd);\n')])]
AXES = [H, L, T, C]
FLAGS = []
