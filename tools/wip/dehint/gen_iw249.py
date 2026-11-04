# attempt 17: on build/iw/a17/bp2.c (writeFsTable's big inner compare left, no dead test): real statements in writeFsTable that may spend or free names: length and end locals, where off is rounded, a second blk, the call's order.
import os
BASE = os.environ.get('IWB', 'build/iw/a17/bp2.c')
D = '	uint32_t blk;\n	int i;\n'
LOG = '	log_printf(1, "offset 0x%x len 0x4000 (end 0x%x)...", off, off + 0x4000);\n'
C1 = 'imgAdd(off, buf, i * 0x400, 0x2c, 0x1ffe, 0);'
C2 = 'imgAdd(off, buf, i * 0x400, 0x30, 0x1ffd, 0);'
TAIL = '	setBeU16(off >> 14, (uint8_t *)&xb.fsBlock);\n'
A = [[('', []),
  ('e1', [(D, D + '	uint32_t end;\n'), (LOG, '	end = off + 0x4000;\n	log_printf(1, "offset 0x%x len 0x4000 (end 0x%x)...", off, end);\n')]),
  ('e2', [(D, D + '	uint32_t len;\n'), (LOG, '	len = i * 0x400;\n	log_printf(1, "offset 0x%x len 0x4000 (end 0x%x)...", off, off + len);\n'), (C1, 'imgAdd(off, buf, len, 0x2c, 0x1ffe, 0);'), (C2, 'imgAdd(off, buf, len, 0x30, 0x1ffd, 0);')]),
  ('e3', [(D, D + '	uint32_t len;\n'), (LOG, '	len = p - buf;\n	log_printf(1, "offset 0x%x len 0x4000 (end 0x%x)...", off, off + len);\n'), (C1, 'imgAdd(off, buf, len, 0x2c, 0x1ffe, 0);'), (C2, 'imgAdd(off, buf, len, 0x30, 0x1ffd, 0);')]),
  ('e4', [(D, D + '	uint32_t len;\n'), (LOG, LOG + '	len = i * 0x400;\n'), (C1, 'imgAdd(off, buf, len, 0x2c, 0x1ffe, 0);'), (C2, 'imgAdd(off, buf, len, 0x30, 0x1ffd, 0);')]),
  ('e5', [(C1, 'imgAdd(off, buf, i * 512 * 2, 0x2c, 0x1ffe, 0);'), (C2, 'imgAdd(off, buf, i * 512 * 2, 0x30, 0x1ffd, 0);')]),
  ('e6', [(C1, 'imgAdd(off, buf, i << 10, 0x2c, 0x1ffe, 0);'), (C2, 'imgAdd(off, buf, i << 10, 0x30, 0x1ffd, 0);')]),
 ],
 [('', []),
  ('t1', [(TAIL, '	blk = off >> 14;\n	setBeU16(blk, (uint8_t *)&xb.fsBlock);\n')]),
  ('t2', [(TAIL, '	setBeU16(blk, (uint8_t *)&xb.fsBlock);\n')]),
  ('t3', [(TAIL, '	setBeU16((uint16_t)(off >> 14), (uint8_t *)&xb.fsBlock);\n')]),
  ('t4', [(TAIL, '	setBeU16(off / 0x4000, (uint8_t *)&xb.fsBlock);\n')]),
 ],
 [('', []),
  ('i1', [('	p = buf;\n	for (i = 0;', '	p = buf;\n	i = 0;\n	for (; i < 16; i++)\n#if 0\n	for (i = 0;'), ('i < 16; i++) {\n		memcpy(p, (uint8_t *)fsTable', 'i < 16; i++)\n#endif\n	{\n		memcpy(p, (uint8_t *)fsTable')]),
  ('i2', [('	uint8_t *buf, *p;\n	uint32_t blk;\n	int i;\n', '	uint8_t *buf, *p;\n	uint32_t blk, i;\n')]),
 ],
]
AXES = A
FLAGS = []
