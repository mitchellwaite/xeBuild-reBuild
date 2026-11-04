# attempt 15, probe only: K names freed by a dead arm in imgAdd on the `&&` partial state (build/iw/a14/foraa.c), to see whether imgAdd's 100 lines are stack position only.
import os
BASE = os.environ.get('IWB', 'build/iw/a14/foraa.c')
POSS = {'a': '	memcpy(xb.hdr + off, src, len);\n', 'b': '	imgEnd = off + len;\n	return 0;\n'}
OPS = ['z += 1;', 'z ^= 3;', 'z <<= 2;', 'z -= 7;', 'z |= 9;', 'z >>= 1;', 'z *= 5;', 'z &= 0xfff;', 'z += len;', 'z ^= len;']
A = []
for lab, ps in POSS.items():
    for k in range(0, 41):
        b = ' '.join(OPS[j % 10] for j in range(k))
        A.append(('%s%d' % (lab, k), [(ps, '	if ((x & 0xff) > 0xff) {\n		uint32_t z = x;\n		%s\n		off = z;\n	}\n' % b + ps)]))
AXES = [A]
FLAGS = []
