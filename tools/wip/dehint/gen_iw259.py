# attempt 18: optimize. Page loop forms that might not get sccp's exit split (notes: FS2 would take the name page loop A takes), natural spellings of the page loop only, on src minus the attribute. Keyed on position 6 of the signature.
# `IWB=build/iw/a18/na.c python tools/wip/dehint/iw16sweep.py tools/wip/dehint/gen_iw259.py -n 20 -t 1`
import os
BASE = os.environ.get('IWB', 'build/iw/a18/na.c')
L = '		for (end = p + npages; p < end; p++) {\n'
A = [('', []),
 ('ne', [(L, '		for (end = p + npages; p != end; p++) {\n')]),
 ('wh', [(L, '		end = p + npages;\n		while (p < end) {\n'), ('							s[7] = len;\n						}\n					}\n				}\n			}\n		}\n', 'XX')]),
 ('cnt', [(L, '		for (end = npages; end != 0; end--, p++) {\n')]),
 ('cn2', [(L, '		for (end = npages; end > 0; end--, p++) {\n')]),
 ('dw', [(L, '		end = p + npages;\n		if (p < end) do {\n'), ('				}\n			}\n		}\n	}\n#undef BLK', 'XX')]),
]
A = [a for a in A if a[0] in ('', 'ne', 'cnt', 'cn2')]
B = [('', []),
 ('sn', [('	uint32_t x, first, rem, tail, blocks, start, p, end, npages, pages;\n', '	uint32_t x, first, rem, tail, blocks, start, p, npages, pages;\n	int end;\n')]),
]
FS = '		for (i = 0; i < blocks; i++) {\n'
C = [('', []),
 ('fne', [(FS, '		for (i = 0; i != blocks; i++) {\n')]),
 ('fgd', [('	if (next != 0xf1f1) {\n\n', '	if (next != 0xf1f1 && blocks) {\n\n')]),
 ('fdw', [(FS, '		i = 0;\n		do {\n'), ('				fsTable[start + i - xb.fsStart] = SWAP16_IMAGE_WRITE(start + i - xb.fsStart + 1);\n			}\n		}\n', '				fsTable[start + i - xb.fsStart] = SWAP16_IMAGE_WRITE(start + i - xb.fsStart + 1);\n			}\n		} while (++i < blocks);\n')]),
]
AXES = [A, B, C]
FLAGS = []
