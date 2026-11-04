# attempt 17, probe only: IWB (src minus optimize) with its dead test swapped for a K-statement dead arm, K = 0..60, by full signature. Tells how many names freed at VRP1 want the optimize-less state.
import os
BASE = os.environ.get('IWB', 'build/iw/a17/na.c')
DEAD = '	if ((off & 0x3fff) > 0x3fff)\n		off += 0x4000;\n'
OPS = ['z += 1;', 'z ^= 3;', 'z <<= 2;', 'z -= 7;', 'z |= 9;', 'z >>= 1;', 'z *= 5;', 'z &= 0xfff;', 'z += off;', 'z ^= off;']
A = [('none', [(DEAD, '')])]
for k in range(0, 61):
    b = ' '.join(OPS[j % 10] for j in range(k))
    A.append(('k%d' % k, [(DEAD, '	if ((off & 0x3fff) > 0x3fff) {\n		uint32_t z = off;\n		%s\n		off = z;\n	}\n' % b)]))
AXES = [A]
FLAGS = []
