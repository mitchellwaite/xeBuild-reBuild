# attempt 11: on build/iw/a10/l1.c.  writeInitialHeader inlines imgAdd(0, &hdrTemplate, ..) by big_speedup: saving 368 of 3574.5, limit 357.  The caller's time also counts and imgWriteHdr is
# inlined into it first (time 1432 then), so instead of cheaper len statements in imgAdd, statements in imgWriteHdr's page loop that survive to the inline estimate raise the denominator: about 105 needed.
# Every form must still compile to imgWriteHdr's code.  Good: writeInitialHeader 0, no call-offset lines.
import os
LOOP = '''	for (b = 0; b < blocks; b++)
		for (p = (start + b) * 32; p < (start + b + 1) * 32; p++) {
			s = (struct sp *)(xb.spare + p * 16);
			memset(s, 0, 16);
			if (xb.bigBlock) {
				s->b2lo = (start + b) >> 8;
				s->b0 = 0xff;
				*((uint8_t *)s + 1) = start + b;
			} else {
				s->b1lo = (start + b) >> 8;
				s->b5 = 0xff;
				*(uint8_t *)s = start + b;
			}
		}
'''
def rep(*pairs):
    t = LOOP
    for a, b in pairs:
        assert a in t, a
        t = t.replace(a, b)
    return [(LOOP, t)]
F = [
 ('', []),
 ('blk', rep(('	for (b = 0; b < blocks; b++)\n		for (p', '	for (b = 0; b < blocks; b++)\n		for (p'), ('(start + b) >> 8', '(p / 32) >> 8'), ('= start + b;', '= p / 32;'))),
 ('blk2', rep(('s->b2lo = (start + b) >> 8', 's->b2lo = (p >> 5) >> 8'), ('*((uint8_t *)s + 1) = start + b', '*((uint8_t *)s + 1) = p >> 5'), ('s->b1lo = (start + b) >> 8', 's->b1lo = (p >> 5) >> 8'), ('*(uint8_t *)s = start + b', '*(uint8_t *)s = p >> 5'))),
 ('ptr', rep(('s = (struct sp *)(xb.spare + p * 16);', '{\n				uint8_t *sb = xb.spare;\n				uint32_t o = p * 16;\n\n				s = (struct sp *)(sb + o);\n			}'))),
 ('loc', rep(('			memset(s, 0, 16);\n', '			blk = start + b;\n			memset(s, 0, 16);\n'), ('(start + b) >> 8', 'blk >> 8'), ('= start + b;', '= blk;'))),
 ('reb', rep(('				s->b2lo = (start + b) >> 8;\n', '				uint32_t blk = start + b;\n\n				s->b2lo = blk >> 8;\n'), ('*((uint8_t *)s + 1) = start + b', '*((uint8_t *)s + 1) = blk'))),
 ('hi', rep(('s->b2lo = (start + b) >> 8', 's->b2lo = ((start + b) >> 8) & 0xf'), ('s->b1lo = (start + b) >> 8', 's->b1lo = ((start + b) >> 8) & 0xf'))),
 ('lo', rep(('*((uint8_t *)s + 1) = start + b', '*((uint8_t *)s + 1) = (start + b) & 0xff'), ('*(uint8_t *)s = start + b', '*(uint8_t *)s = (start + b) & 0xff'))),
 ('hilo', rep(('s->b2lo = (start + b) >> 8', 's->b2lo = ((start + b) >> 8) & 0xf'), ('s->b1lo = (start + b) >> 8', 's->b1lo = ((start + b) >> 8) & 0xf'), ('*((uint8_t *)s + 1) = start + b', '*((uint8_t *)s + 1) = (start + b) & 0xff'), ('*(uint8_t *)s = start + b', '*(uint8_t *)s = (start + b) & 0xff'))),
 ('st', rep(('			memset(s, 0, 16);\n', '			memset(s, 0, sizeof(*s) + 0);\n'))),
 ('wh', [('	for (b = 0; b < blocks; b++)\n		for (p = (start + b) * 32; p < (start + b + 1) * 32; p++) {', '	for (b = 0; b < blocks; b++) {\n		uint32_t last = (start + b + 1) * 32;\n\n		for (p = (start + b) * 32; p < last; p++) {'), ('				*(uint8_t *)s = start + b;\n			}\n		}\n	imgEnd', '				*(uint8_t *)s = start + b;\n			}\n		}\n	}\n	imgEnd')]),
]
AXES = [F]
BASE = os.environ.get('IWB', 'build/iw/a10/l1.c')
FLAGS = []
