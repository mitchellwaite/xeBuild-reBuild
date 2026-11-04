# attempt 14: writeFsTable's length (i * 0x400 is the only thing keeping len unknown at inlining) x loop, attribute on/off, on near13. p - buf and a running size are the natural readings.
import os
BASE = os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_near13.c')
ATTR = '__attribute__((optimize("no-tree-scev-cprop"))) void writeFsTable'
DECL = '	uint8_t *p, *buf;\n	uint32_t blk;\n	int i;\n'
LOOP = '''	for (i = 0; i < 16; i++) {
		memcpy(p, (uint8_t *)fsTable + i * 0x200, 0x200);
		p += 0x200;
		memcpy(p, (uint8_t *)fsFiles + i * 0x200, 0x200);
		p += 0x200;
	}
'''
B = '	imgAdd(off, buf, i * 0x400, 0x2c, 0x1ffe, 0);\n'
S = '	imgAdd(off, buf, i * 0x400, 0x30, 0x1ffd, 0);\n'
def ln(lab, e, decl='', loop=None):
    ed = [(B, B.replace('i * 0x400', e)), (S, S.replace('i * 0x400', e))]
    if decl:
        ed.append((DECL, DECL + decl))
    if loop:
        ed.append((LOOP, loop))
    return (lab, ed)
L_SIZE = LOOP.replace('		p += 0x200;\n	}\n', '		p += 0x200;\n		size += 0x400;\n	}\n')
L_SZ2 = LOOP.replace('		p += 0x200;\n		memcpy', '		size += 0x200;\n		p += 0x200;\n		memcpy').replace('		p += 0x200;\n	}\n', '		p += 0x200;\n		size += 0x200;\n	}\n')
AX = [('', []),
 ln('pb', 'p - buf'),
 ln('pbu', '(uint32_t)(p - buf)'),
 ln('sh', 'i << 10'),
 ln('m2', '0x400 * i'),
 ln('m3', 'i * 2 * 0x200'),
 ln('sz', 'size', '	uint32_t size = 0;\n', L_SIZE),
 ln('sz2', 'size', '	uint32_t size = 0;\n', L_SZ2),
 ln('k', 'size', '	uint32_t size = 0x4000;\n'),
 ln('pl', 'n', '	uint32_t n;\n', LOOP + '	n = p - buf;\n'),
 ln('il', 'n', '	uint32_t n;\n', LOOP + '	n = i * 0x400;\n'),
]
AT = [('', []), ('noattr', [(ATTR, 'void writeFsTable')])]
ST = '	fsTable[-xb.fsStart + blk] = SWAP16_IMAGE_WRITE(0x1ffd);\n'
TL = '	setBeU16(off >> 14, (uint8_t *)&xb.fsBlock);\n'
AXES = [AX, AT,
 [('', []), ('st0', [(ST, '	fsTable[blk - xb.fsStart] = SWAP16_IMAGE_WRITE(0x1ffd);\n')])],
 [('', []), ('t0', [(TL, '	setBeU16(blk, (uint8_t *)&xb.fsBlock);\n')])],
]
FLAGS = []
