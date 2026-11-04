# attempt 15, probe only: gen_iw220 with K up to 80, one position. Result is a function of K, not of position, so one is enough. IWB= other base.
import os
BASE = os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_a14.c')
ps = '	if (!xb.bigBlock)\n		goto small;\n'
OPS = ['z += 1;', 'z ^= 3;', 'z <<= 2;', 'z -= 7;', 'z |= 9;', 'z >>= 1;', 'z *= 5;', 'z &= 0xfff;', 'z += off;', 'z ^= off;']
A = []
for k in range(0, 81):
    b = ' '.join(OPS[j % 10] for j in range(k))
    A.append(('k%d' % k, [(ps, '	if ((off & 0x3fff) > 0x3fff) {\n		uint32_t z = off;\n		%s\n		off = z;\n	}\n' % b + ps)]))
AXES = [A]
FLAGS = []
