# attempt 11: on build/iw/a11/g1.c: writeInitialHeader's inline.  g1 saves 363 of 3569.5 (10.17%): the denominator needs +61 or the saving -6.  Forms of imgWriteHdr's page loop (the block number from p, which reads naturally since the loop runs on absolute page numbers)
# and of imgAdd's pg statement.  Read with iw11inl.py; good = writeInitialHeader lines down to the call offsets.
import os
BASE = os.environ.get('IWB', 'build/iw/a11/g1.c')
LOOP = '''			s = (struct sp *)(xb.spare + p * 16);
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
'''
def body(lo, hi, pre=''):
    return pre + '''			s = (struct sp *)(xb.spare + p * 16);
			memset(s, 0, 16);
			if (xb.bigBlock) {
				s->b2lo = %s;
				s->b0 = 0xff;
				*((uint8_t *)s + 1) = %s;
			} else {
				s->b1lo = %s;
				s->b5 = 0xff;
				*(uint8_t *)s = %s;
			}
''' % (hi, lo, hi, lo)
F = [
 ('', []),
 ('a', [(LOOP, body('p / 32', '(p / 32) >> 8'))]),
 ('b', [(LOOP, body('p / 32', 'p / 8192'))]),
 ('c', [(LOOP, body('p / 32', 'p / 32 / 256'))]),
 ('d', [(LOOP, body('lba', 'lba >> 8', '			uint32_t lba = p / 32;\n\n').replace('			uint32_t lba = p / 32;\n\n', '')), ('	struct sp *s;\n\n	if (off > xb.rawSize', '	struct sp *s;\n	uint32_t lba;\n\n	if (off > xb.rawSize'), ('			s = (struct sp *)(xb.spare + p * 16);\n', '			lba = p / 32;\n			s = (struct sp *)(xb.spare + p * 16);\n')]),
 ('e', [(LOOP, body('p / 32', '(p >> 5) >> 8'))]),
 ('f', [(LOOP, body('p >> 5', 'p / 32 >> 8'))]),
 ('g', [(LOOP, body('p / 32', '(p / 32) / 256'))]),
 ('h', [(LOOP, body('(p - p % 32) / 32', '((p - p % 32) / 32) >> 8'))]),
 ('i', [(LOOP, body('p / 32 + start', '(p / 32 + start) >> 8'))]),
]
AXES = [F]
FLAGS = []
