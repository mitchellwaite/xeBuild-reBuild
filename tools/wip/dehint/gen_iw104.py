# attempt 6: r0: the loops' counters: block number as its own iv, FS loop over block numbers, loop bound in a local (more or fewer names pre-ivopts)
import os
OUT = '	for (b = 0; b < blocks; b++) {\n'
BLKD = '#define BLK (start + b)\n'
FS = '''		for (i = 0; i < blocks; i++) {
			if (next != 0 && next != 0xffff) {
				fsTable[start + i - xb.fsStart] = SWAP16_IMAGE_WRITE(next);
			} else {
				fsTable[start + i - xb.fsStart] = SWAP16_IMAGE_WRITE(start + i - xb.fsStart + 1);
			}
		}
'''
FX = {
 'i1': '''		for (i = start; i < start + blocks; i++) {
			if (next != 0 && next != 0xffff) {
				fsTable[i - xb.fsStart] = SWAP16_IMAGE_WRITE(next);
			} else {
				fsTable[i - xb.fsStart] = SWAP16_IMAGE_WRITE(i - xb.fsStart + 1);
			}
		}
''',
 'i2': '''		end = start + blocks;
		for (i = start; i < end; i++) {
			if (next != 0 && next != 0xffff) {
				fsTable[i - xb.fsStart] = SWAP16_IMAGE_WRITE(next);
			} else {
				fsTable[i - xb.fsStart] = SWAP16_IMAGE_WRITE(i - xb.fsStart + 1);
			}
		}
''',
 'i3': '''		for (i = 0; i != blocks; i++) {
			if (next != 0 && next != 0xffff) {
				fsTable[start + i - xb.fsStart] = SWAP16_IMAGE_WRITE(next);
			} else {
				fsTable[start + i - xb.fsStart] = SWAP16_IMAGE_WRITE(start + i - xb.fsStart + 1);
			}
		}
''',
 'i4': '''		i = 0;
		do {
			if (next != 0 && next != 0xffff) {
				fsTable[start + i - xb.fsStart] = SWAP16_IMAGE_WRITE(next);
			} else {
				fsTable[start + i - xb.fsStart] = SWAP16_IMAGE_WRITE(start + i - xb.fsStart + 1);
			}
		} while (++i < blocks);
''',
 'i5': '''		for (i = 0; i < blocks; i++) {
			if (next != 0 && next != 0xffff)
				fsTable[start + i - xb.fsStart] = SWAP16_IMAGE_WRITE(next);
			else
				fsTable[start + i - xb.fsStart] = SWAP16_IMAGE_WRITE((start + i) - xb.fsStart + 1);
		}
''',
 'i6': '''		for (i = 0; i < blocks; i++) {
			if (next == 0 || next == 0xffff) {
				fsTable[start + i - xb.fsStart] = SWAP16_IMAGE_WRITE(start + i - xb.fsStart + 1);
			} else {
				fsTable[start + i - xb.fsStart] = SWAP16_IMAGE_WRITE(next);
			}
		}
''',
}
AXES = [
 [('', [])] + [(k, [(FS, v)]) for k, v in FX.items()],
 [('', []),
  ('bv', [(BLKD, '#define BLK blk\n'), (OUT, '	for (blk = start, b = 0; b < blocks; b++, blk++) {\n'), ('	uint32_t b;\n', '	uint32_t b, blk;\n')]),
  ('bw', [(BLKD, '#define BLK b\n'), (OUT, '	for (b = start; b < start + blocks; b++) {\n'),
          ('(pg + p + b * 32)', '(pg + p + (b - start) * 32)')]),
  ('bx', [(OUT, '	for (b = 0; b != blocks; b++) {\n')]),
 ],
]
BASE = os.environ.get('IWB', 'build/iw/a6/r0.c')
FLAGS = []
