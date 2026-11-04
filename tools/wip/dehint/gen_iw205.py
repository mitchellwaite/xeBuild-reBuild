# attempt 13: writeFsTable on near13 (w2, one compare left with the dead test gone), natural named values that iw8wf doesn't try: end, a table index, its own pointer IVs.
import os
BASE = os.environ.get('IWB', 'build/iw/a13/w2.c')
ATTR = '__attribute__((optimize("no-tree-scev-cprop"))) void writeFsTable'
DECL = '	uint8_t *p, *buf;\n	uint32_t blk;\n	int i;\n'
ST = '	fsTable[-xb.fsStart + blk] = SWAP16_IMAGE_WRITE(0x1ffd);\n'
LOG = '	log_printf(1, "offset 0x%x len 0x4000 (end 0x%x)...", off, off + 0x4000);\n'
TAIL = '	setBeU16(off >> 14, (uint8_t *)&xb.fsBlock);\n'
HEAD = '''	blk = off >> 14;
	if (xb.bigBlock && (off & 0x1ffff)) {
		off = (off + 0x20000) & ~0x1ffff;
		blk = off >> 14;
	}
'''
LOOP = '''		memcpy(p, (uint8_t *)fsTable + i * 0x200, 0x200);
		p += 0x200;
		memcpy(p, (uint8_t *)fsFiles + i * 0x200, 0x200);
		p += 0x200;
'''
CALLB = '	imgAdd(off, buf, i * 0x400, 0x2c, 0x1ffe, 0);\n'
CALLS = '	imgAdd(off, buf, i * 0x400, 0x30, 0x1ffd, 0);\n'
AXES = [
 [('', []), ('noattr', [(ATTR, 'void writeFsTable')])],
 [('', []),
  ('st0', [(ST, '	fsTable[blk - xb.fsStart] = SWAP16_IMAGE_WRITE(0x1ffd);\n')]),
  ('st1', [(ST, '	i = blk - xb.fsStart;\n	fsTable[i] = SWAP16_IMAGE_WRITE(0x1ffd);\n')]),
  ('st2', [(ST, '	fsTable[(off >> 14) - xb.fsStart] = SWAP16_IMAGE_WRITE(0x1ffd);\n')]),
 ],
 [('', []),
  ('e1', [(DECL, DECL + '	uint32_t end;\n'), (LOG, '	end = off + 0x4000;\n	log_printf(1, "offset 0x%x len 0x4000 (end 0x%x)...", off, end);\n')]),
  ('e2', [(DECL, DECL + '	uint32_t size = 0x4000;\n'), (LOG, '	log_printf(1, "offset 0x%x len 0x%x (end 0x%x)...", off, size, off + size);\n'.replace('len 0x%x', 'len 0x4000').replace(', size, off', ', off'))]),
 ],
 [('', []),
  ('h1', [(HEAD, '	if (xb.bigBlock && (off & 0x1ffff))\n		off = (off + 0x20000) & ~0x1ffff;\n	blk = off >> 14;\n')]),
  ('h2', [(HEAD, '	blk = off >> 14;\n	if (xb.bigBlock) {\n		if (off & 0x1ffff) {\n			off = (off + 0x20000) & ~0x1ffff;\n			blk = off >> 14;\n		}\n	}\n')]),
 ],
 [('', []),
  ('l1', [(LOOP, '		memcpy(p, (uint8_t *)fsTable + i * 0x200, 0x200);\n		memcpy(p + 0x200, (uint8_t *)fsFiles + i * 0x200, 0x200);\n		p += 0x400;\n')]),
  ('l2', [(LOOP, '		memcpy(p, (uint8_t *)fsTable + i * 512, 512);\n		p += 512;\n		memcpy(p, (uint8_t *)fsFiles + i * 512, 512);\n		p += 512;\n')]),
  ('l3', [(LOOP, '		memcpy(p, &fsTable[i * 0x100], 0x200);\n		p += 0x200;\n		memcpy(p, (uint8_t *)fsFiles + i * 0x200, 0x200);\n		p += 0x200;\n')]),
 ],
 [('', []),
  ('t0', [(TAIL, '	setBeU16(blk, (uint8_t *)&xb.fsBlock);\n')]),
 ],
]
FLAGS = []
