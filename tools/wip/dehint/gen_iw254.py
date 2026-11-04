# attempt 18: optimize. writeFsTable-local real shapes crossed on src minus the attribute (IWB=build/iw/a18/na.c). Linux reads as if/else calls and `lea r10,[r9+0x200]; add r9,0x400`.
# `IWB=build/iw/a18/na.c python tools/wip/dehint/iw16sweep.py tools/wip/dehint/gen_iw254.py -n 30 -t 3`.
import os
BASE = os.environ.get('IWB', 'build/iw/a18/na.c')
G = '	if (!xb.bigBlock)\n		goto small;\n	imgAdd(off, buf, len, 0x2c, 0x1ffe, 0);\n	goto done;\nsmall:\n	imgAdd(off, buf, len, 0x30, 0x1ffd, 0);\ndone:\n'
CALL = [('', []),
 ('ie', [(G, '	if (xb.bigBlock)\n		imgAdd(off, buf, len, 0x2c, 0x1ffe, 0);\n	else\n		imgAdd(off, buf, len, 0x30, 0x1ffd, 0);\n')]),
 ('ni', [(G, '	if (!xb.bigBlock)\n		imgAdd(off, buf, len, 0x30, 0x1ffd, 0);\n	else\n		imgAdd(off, buf, len, 0x2c, 0x1ffe, 0);\n')]),
 ('gd', [(G, '	if (!xb.bigBlock) {\n		imgAdd(off, buf, len, 0x30, 0x1ffd, 0);\n		goto done;\n	}\n	imgAdd(off, buf, len, 0x2c, 0x1ffe, 0);\ndone:\n')]),
]
LP = '''	for (i = 0; i < 16; i++) {
		memcpy(p, (uint8_t *)fsTable + i * 0x200, 0x200);
		p += 0x200;
		memcpy(p, (uint8_t *)fsFiles + i * 0x200, 0x200);
		p += 0x200;
	}
'''
LOOP = [('', []),
 ('l2', [(LP, '''	for (i = 0; i < 16; i++) {
		memcpy(p, (uint8_t *)fsTable + i * 0x200, 0x200);
		memcpy(p + 0x200, (uint8_t *)fsFiles + i * 0x200, 0x200);
		p += 0x400;
	}
''')]),
 ('l3', [(LP, '''	for (i = 0; i < 16; i++) {
		memcpy(buf + i * 0x400, (uint8_t *)fsTable + i * 0x200, 0x200);
		memcpy(buf + i * 0x400 + 0x200, (uint8_t *)fsFiles + i * 0x200, 0x200);
	}
''')]),
 ('l4', [(LP, '''	for (i = 0; i < 16; i++) {
		memcpy(p, (uint8_t *)fsTable + i * 0x200, 0x200);
		memcpy(&p[0x200], (uint8_t *)fsFiles + i * 0x200, 0x200);
		p += 0x400;
	}
''')]),
 ('l5', [(LP, '''	for (i = 0; i < 16; i++) {
		memcpy(p, &((uint8_t *)fsTable)[i * 0x200], 0x200);
		p += 0x200;
		memcpy(p, &((uint8_t *)fsFiles)[i * 0x200], 0x200);
		p += 0x200;
	}
''')]),
]
LE = '	len = i * 0x400;\n	log_printf(1, "offset 0x%x len 0x4000 (end 0x%x)...", off, off + len);\n'
LEN = [('', []),
 ('e1', [(LE, '	len = p - buf;\n	log_printf(1, "offset 0x%x len 0x4000 (end 0x%x)...", off, off + len);\n')]),
 ('e2', [(LE, '	log_printf(1, "offset 0x%x len 0x4000 (end 0x%x)...", off, off + 0x4000);\n	len = i * 0x400;\n')]),
 ('e3', [(LE, '	len = i * 0x400;\n	end = off + len;\n	log_printf(1, "offset 0x%x len 0x4000 (end 0x%x)...", off, end);\n'), ('	uint32_t len;\n', '	uint32_t len, end;\n')]),
 ('e4', [(LE, '	len = i * 0x200 * 2;\n	log_printf(1, "offset 0x%x len 0x4000 (end 0x%x)...", off, off + len);\n')]),
]
TAIL = [('', []),
 ('t1', [('	setBeU16(blk, (uint8_t *)&xb.fsBlock);\n', '	setBeU16(off >> 14, (uint8_t *)&xb.fsBlock);\n')]),
]
IT = [('', []), ('ui', [('	uint8_t *buf, *p;\n	uint32_t blk;\n	int i;\n', '	uint8_t *buf, *p;\n	uint32_t blk;\n	uint32_t i;\n')])]
AXES = [CALL, LOOP, LEN, TAIL, IT]
FLAGS = []
