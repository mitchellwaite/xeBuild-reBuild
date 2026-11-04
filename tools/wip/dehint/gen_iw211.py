# attempt 13: near13 (w2) and w2na: is one hint in writeFsTable enough for the last compare? Net count would still fall: lnp2 and the dead test gone, one new hint. asm uses x position; `(void)`-like plain locals first.
import os
BASE = os.environ.get('IWB', 'build/iw/a13/w2.c')
POS = ['	buf = malloc(0x4000);\n', '	p = buf;\n', '	for (i = 0; i < 16; i++) {\n		memcpy(p, (uint8_t *)fsTable', '	log_printf(1, "offset 0x%x len 0x4000', '	if (!xb.bigBlock)\n		goto small;\n',
       '	imgAdd(off, buf, i * 0x400, 0x2c, 0x1ffe, 0);\n', '	imgAdd(off, buf, i * 0x400, 0x30, 0x1ffd, 0);\n', '	setBeU16(off >> 14, (uint8_t *)&xb.fsBlock);\n', '	setBeU16(0, (uint8_t *)&xb.fsReserved);\n', '	free(buf);\n	}XX']
USES = ['off', 'blk', 'i', 'buf', 'p', 'off >> 14', 'off + 0x4000', 'i * 0x400', 'xb.bigBlock']
A = [('', [])]
for pi, ps in enumerate(POS):
    if 'XX' in ps:
        continue
    for ui, u in enumerate(USES):
        for c in 'gr':
            A.append(('p%du%d%s' % (pi, ui, c), [(ps, '	__asm__("" :: "%s"(%s));\n' % (c, u) + ps)]))
AXES = [A]
FLAGS = []
