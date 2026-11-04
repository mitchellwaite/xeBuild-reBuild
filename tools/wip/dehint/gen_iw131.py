# attempt 8: n2 (lnp2 and pin_t gone, `unsigned t`, 50/50 npages): writeInitialHeader inlines its off-0x80, next-0xf1f1 call because the saving is 10.17% (limit 10%).
# Forms of the FS loop and of the page loop that save a little less or cost a little more in the inline estimate.
import os
FLAGS = []
BASE = os.environ.get('IWB', 'build/iw/a8/n2.c')
FOCUS = ['_imgAdd', '_imgAdd.constprop.1', '_imgAdd.constprop.2', '_imgAdd.constprop.4', '_imgAddFile', '_writeInitialHeader']
FS = '''			if (next != 0 && next != 0xffff) {
				fsTable[start + i - xb.fsStart] = SWAP16_IMAGE_WRITE(next);
			} else {
				fsTable[start + i - xb.fsStart] = SWAP16_IMAGE_WRITE(start + i - xb.fsStart + 1);
			}
'''
FSF = [
 ('', []),
 ('fa', [(FS, '''			uint16_t v;

			if (next != 0 && next != 0xffff)
				v = next;
			else
				v = start + i - xb.fsStart + 1;
			fsTable[start + i - xb.fsStart] = SWAP16_IMAGE_WRITE(v);
''')]),
 ('fb', [(FS, '''			uint32_t k = start + i - xb.fsStart;

			if (next != 0 && next != 0xffff)
				fsTable[k] = SWAP16_IMAGE_WRITE(next);
			else
				fsTable[k] = SWAP16_IMAGE_WRITE(k + 1);
''')]),
 ('fc', [(FS, '''			if (next == 0 || next == 0xffff) {
				fsTable[start + i - xb.fsStart] = SWAP16_IMAGE_WRITE(start + i - xb.fsStart + 1);
			} else {
				fsTable[start + i - xb.fsStart] = SWAP16_IMAGE_WRITE(next);
			}
''')]),
 ('fd', [(FS, '''			if (next != 0 && next != 0xffff)
				fsTable[start - xb.fsStart + i] = SWAP16_IMAGE_WRITE(next);
			else
				fsTable[start - xb.fsStart + i] = SWAP16_IMAGE_WRITE(start - xb.fsStart + i + 1);
''')]),
 ('fe', [('		for (i = 0; i < blocks; i++) {\n' + FS + '		}\n', '''		if (next != 0 && next != 0xffff) {
			for (i = 0; i < blocks; i++)
				fsTable[start + i - xb.fsStart] = SWAP16_IMAGE_WRITE(next);
		} else {
			for (i = 0; i < blocks; i++)
				fsTable[start + i - xb.fsStart] = SWAP16_IMAGE_WRITE(start + i - xb.fsStart + 1);
		}
''')]),
]
S = '''			pg = start * 32;
			s = xb.spare + (pg + p + b * 32) * 16;
'''
PGF = [
 ('', []),
 ('g1', [(S, '			pg = (start + b) * 32;\n			s = xb.spare + (pg + p) * 16;\n')]),
 ('g2', [(S, '			pg = BLK * 32;\n			s = xb.spare + (pg + p) * 16;\n')]),
 ('g3', [(S, '			pg = start * 32;\n			s = xb.spare + (pg + b * 32) * 16 + p * 16;\n')]),
 ('g4', [(S, '			pg = start * 32 + p;\n			s = xb.spare + (pg + b * 32) * 16;\n')]),
 ('g5', [(S, '			pg = start * 512;\n			s = xb.spare + pg + (p + b * 32) * 16;\n')]),
 ('g6', [(S, '			pg = start * 512;\n			s = xb.spare + pg + p * 16 + b * 512;\n')]),
 ('g7', [(S, '			pg = start * 32;\n			s = xb.spare + pg * 16 + p * 16 + b * 512;\n')]),
]
PG = '			pages = len % 512 ? len / 512 + 1 : len / 512;\n'
PF = [
 ('', []),
 ('h1', [(PG, '			pages = len / 512;\n			if (len % 512)\n				pages++;\n')]),
 ('h2', [(PG, '			if (len % 512)\n				pages = len / 512 + 1;\n			else\n				pages = len / 512;\n')]),
]
AXES = [FSF, PGF, PF]
