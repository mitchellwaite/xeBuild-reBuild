# attempt 13: imgAdd's FS table chain on near13 (w2). In writeFsTable's big copy the compare's inc name is `start + i` of this code, released at ccp2, so its spelling is the next thing to move.
import os
BASE = os.environ.get('IWB', 'build/iw/a13/w2.c')
OLD = '''		for (i = 0; i < blocks; i++) {
			if (next != 0 && next != 0xffff) {
				fsTable[start + i - xb.fsStart] = SWAP16_IMAGE_WRITE(next);
			} else {
				fsTable[start + i - xb.fsStart] = SWAP16_IMAGE_WRITE(start + i - xb.fsStart + 1);
			}
		}
		if (next == 0xffff) {
			fsTable[start - xb.fsStart + blocks - 1] = SWAP16_IMAGE_WRITE(0x1fff);
		}
'''
def F(a1, a2, v, t):
    return '''		for (i = 0; i < blocks; i++) {
			if (next != 0 && next != 0xffff) {
				fsTable[%s] = SWAP16_IMAGE_WRITE(next);
			} else {
				fsTable[%s] = SWAP16_IMAGE_WRITE(%s);
			}
		}
		if (next == 0xffff) {
			fsTable[%s] = SWAP16_IMAGE_WRITE(0x1fff);
		}
''' % (a1, a2, v, t)
I1 = ['start + i - xb.fsStart', 'i + start - xb.fsStart', '(start + i) - xb.fsStart', 'start - xb.fsStart + i', 'i - xb.fsStart + start']
V = ['start + i - xb.fsStart + 1', 'i + start - xb.fsStart + 1', 'start - xb.fsStart + i + 1', 'start + i + 1 - xb.fsStart', '1 + start + i - xb.fsStart', 'start + (i + 1) - xb.fsStart']
T = ['start - xb.fsStart + blocks - 1', 'start + blocks - 1 - xb.fsStart', 'start + blocks - xb.fsStart - 1', 'blocks + start - xb.fsStart - 1']
A = []
for a, x in enumerate(I1):
    for b, y in enumerate(I1):
        for c, z in enumerate(V):
            for d, w in enumerate(T):
                A.append(('a%db%dc%dd%d' % (a, b, c, d), [(OLD, F(x, y, z, w))]))
EX = [
 ('n1', [(OLD, '''		for (i = 0; i < blocks; i++) {
			uint32_t e = start + i - xb.fsStart;

			if (next != 0 && next != 0xffff)
				fsTable[e] = SWAP16_IMAGE_WRITE(next);
			else
				fsTable[e] = SWAP16_IMAGE_WRITE(e + 1);
		}
		if (next == 0xffff) {
			fsTable[start - xb.fsStart + blocks - 1] = SWAP16_IMAGE_WRITE(0x1fff);
		}
''')]),
 ('n2', [(OLD, '''		for (i = start; i < start + blocks; i++) {
			if (next != 0 && next != 0xffff)
				fsTable[i - xb.fsStart] = SWAP16_IMAGE_WRITE(next);
			else
				fsTable[i - xb.fsStart] = SWAP16_IMAGE_WRITE(i - xb.fsStart + 1);
		}
		if (next == 0xffff) {
			fsTable[start - xb.fsStart + blocks - 1] = SWAP16_IMAGE_WRITE(0x1fff);
		}
''')]),
]
AXES = [A + EX]
FLAGS = []
