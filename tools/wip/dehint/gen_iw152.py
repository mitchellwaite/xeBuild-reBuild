# attempt 9: requirement (B) of pin_hdr.  Base build/iw/a9/ex.c at expect 75 stands in for requirement (A) (head freq >= 350): only the hdr/spare swap
# is left (57 lines).  The swap is a tie on the pseudo number, i.e. the lowest SSA name of each PHI partition.  Natural forms of finalizeImage that move
# PRE's free names; IDENTICAL here proves (A) + (B) is enough.
import os
BC = '''			uint8_t t;

			if (!spareUsed(xb.spare + i * 16))
				continue;
			t = xb.spare[i * 16];
'''
BIG = '''		spare = xb.spare;
		for (b = 0; b < n; b++)
			for (p = 0; p < 256; p++) {
				s = spare + b * 0x1000 + p * 16;
'''
MAL = '''	xb.raw = (uint8_t *)(mem = xmalloc(xb.rawSize));
	if (!mem)
		return -1;
'''
TEST = '''			if (__builtin_expect(!pageErased(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16), 0))
				calcPageEcc(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16);
			memcpy(raw, xb.hdr + (b * 32 + p) * 512, 512);
			memcpy(raw + 512, xb.spare + (b * 32 + p) * 16, 16);
'''
AXES = [
 [('', []),
  ('bc1', [(BC, '''			uint8_t t;

			if (spareUsed(xb.spare + i * 16)) {
			t = xb.spare[i * 16];
'''), ('''			xb.spare[i * 16 + 1] = t;
''', '''			xb.spare[i * 16 + 1] = t;
			}
''')]),
  ('bc2', [(BC, '''			uint8_t t = xb.spare[i * 16];

			if (!spareUsed(xb.spare + i * 16))
				continue;
''')]),
  ('bc3', [('''			xb.spare[i * 16] = xb.spare[i * 16 + 2];
''', '''			t2 = xb.spare[i * 16 + 2];
			xb.spare[i * 16] = t2;
'''), ('			uint8_t t;\n', '			uint8_t t, t2;\n')]),
 ],
 [('', []),
  ('big1', [(BIG, '''		for (b = 0; b < n; b++)
			for (p = 0; p < 256; p++) {
				s = xb.spare + b * 0x1000 + p * 16;
''')]),
  ('big2', [(BIG, '''		spare = xb.spare;
		for (b = 0; b < n; b++)
			for (p = 0; p < 256; p++) {
				s = spare + (b * 256 + p) * 16;
''')]),
 ],
 [('', []),
  ('mal1', [(MAL, '''	mem = xmalloc(xb.rawSize);
	xb.raw = (uint8_t *)mem;
	if (!mem)
		return -1;
''')]),
 ],
 [('', []),
  ('n1', [(TEST, '''			n = b * 32 + p;
			if (__builtin_expect(!pageErased(xb.hdr + n * 512, xb.spare + n * 16), 0))
				calcPageEcc(xb.hdr + n * 512, xb.spare + n * 16);
			memcpy(raw, xb.hdr + n * 512, 512);
			memcpy(raw + 512, xb.spare + n * 16, 16);
''')]),
  ('n2', [(TEST, '''			if (__builtin_expect(!pageErased(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16), 0))
				calcPageEcc(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16);
			n = b * 32 + p;
			memcpy(raw, xb.hdr + n * 512, 512);
			memcpy(raw + 512, xb.spare + n * 16, 16);
''')]),
  ('o1', [(TEST, '''			if (__builtin_expect(!pageErased(xb.hdr + b * 32 * 512 + p * 512, xb.spare + (b * 32 + p) * 16), 0))
				calcPageEcc(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16);
			memcpy(raw, xb.hdr + (b * 32 + p) * 512, 512);
			memcpy(raw + 512, xb.spare + (b * 32 + p) * 16, 16);
''')]),
 ],
 [('', []),
  ('bb1', [('''		log_printf(1, "fixing up big block LBA numbers in spare...");
		n = xb.blocks / 8;
''', '''		log_printf(1, "fixing up big block LBA numbers in spare...");
		i = xb.blocks / 8;
'''), ('		for (b = 0; b < n; b++)\n			for (p = 0; p < 256; p++) {\n', '		for (b = 0; b < i; b++)\n			for (p = 0; p < 256; p++) {\n')]),
 ],
 [('', []),
  ('mu1', [('''		raw = xb.raw + xb.spare7 * 0x21000;
		for (b = xb.spare7; b < xb.muBlocks; b++)
''', '''		b = xb.spare7;
		raw = xb.raw + b * 0x21000;
		for (; b < xb.muBlocks; b++)
''')]),
 ],
]
BASE = 'build/iw/a9/ex.c'
FLAGS = ['--param', 'builtin-expect-probability=75']
FOCUS = ['_finalizeImage']
