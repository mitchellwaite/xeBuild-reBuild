# attempt 14: imgAdd's FS chain as one store of a chosen value. Rejudge found gen_iw52 `v9` (a ternary inside the store) leaves writeFsTable clean, cost constprop.1 3 flips, imgAdd's 2 slots, constprop.2 104.
import os
BASE = os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_a14.c')
OLD = '''			if (next != 0 && next != 0xffff) {
				fsTable[start + i - xb.fsStart] = SWAP16_IMAGE_WRITE(next);
			} else {
				fsTable[start + i - xb.fsStart] = SWAP16_IMAGE_WRITE(start + i - xb.fsStart + 1);
			}
'''
C = 'next != 0 && next != 0xffff'
N = '(next == 0 || next == 0xffff)'
A = 'SWAP16_IMAGE_WRITE(next)'
B = 'SWAP16_IMAGE_WRITE(start + i - xb.fsStart + 1)'
I = 'start + i - xb.fsStart'
D = '			uint16_t v;\n\n'
F = {
 '': None,
 'v9': '			fsTable[%s] = %s ? %s : %s;\n' % (I, C, A, B),
 'vn': '			fsTable[%s] = %s ? %s : %s;\n' % (I, N, B, A),
 'v1': '			uint16_t v = %s ? %s : %s;\n\n			fsTable[%s] = v;\n' % (C, A, B, I),
 'v2': '			uint16_t v = %s ? %s : %s;\n\n			fsTable[%s] = v;\n' % (N, B, A, I),
 'i1': D + '			if (%s)\n				v = %s;\n			else\n				v = %s;\n			fsTable[%s] = v;\n' % (C, A, B, I),
 'i2': D + '			if (%s)\n				v = %s;\n			else\n				v = %s;\n			fsTable[%s] = v;\n' % (N, B, A, I),
 'u1': '			uint32_t k = %s;\n\n			fsTable[k] = %s ? %s : SWAP16_IMAGE_WRITE(k + 1);\n' % (I, C, A),
 'u2': '			uint32_t k = %s;\n\n			if (%s)\n				fsTable[k] = %s;\n			else\n				fsTable[k] = SWAP16_IMAGE_WRITE(k + 1);\n' % (I, C, A),
 'w1': '			fsTable[%s] = SWAP16_IMAGE_WRITE(%s ? next : %s + 1);\n' % (I, C, I),
 'w2': '			uint32_t n = %s ? next : %s + 1;\n\n			fsTable[%s] = SWAP16_IMAGE_WRITE(n);\n' % (C, I, I),
 'w3': '			uint16_t n = %s ? next : %s + 1;\n\n			fsTable[%s] = SWAP16_IMAGE_WRITE(n);\n' % (C, I, I),
}
AXES = [[(k, [(OLD, v)] if v else []) for k, v in F.items()]]
FLAGS = []
