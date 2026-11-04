# attempt 17, probe only: K-statement dead arm (replacing the dead test; K=-1 keeps src's) x M partially redundant `off >> n` (PRE PHIs live until later) on IWB, by full signature. Is the target reachable without optimize at all?
import os
BASE = os.environ.get('IWB', 'build/iw/a17/na.c')
DEAD = '	if ((off & 0x3fff) > 0x3fff)\n		off += 0x4000;\n'
OPS = ['z += 1;', 'z ^= 3;', 'z <<= 2;', 'z -= 7;', 'z |= 9;', 'z >>= 1;', 'z *= 5;', 'z &= 0xfff;', 'z += off;', 'z ^= off;']
A1 = '	blk = off >> 14;\n	if (xb.bigBlock && (off & 0x1ffff)) {\n		off = (off + 0x20000) & ~0x1ffff;\n		blk = off >> 14;\n	}\n'
E_ = '	setBeU16(0, (uint8_t *)&xb.fsReserved);\n'
D0 = '	uint32_t blk;\n	int i;\n\n	blk = off >> 14;'
K = [('kd', [])]
for k in range(0, 13):
    b = ' '.join(OPS[j % 10] for j in range(k))
    K.append(('k%d' % k, [(DEAD, '	if ((off & 0x3fff) > 0x3fff) {\n		uint32_t z = off;\n		%s\n		off = z;\n	}\n' % b)] if k else [(DEAD, '')]))
M = [('m0', [])]
for m in range(1, 6):
    u = ['u%d' % i for i in range(m)]
    new = '	blk = off >> 14;\n' + ''.join('	%s = off >> %d;\n' % (n, 13 - i) for i, n in enumerate(u)) + '	if (xb.bigBlock && (off & 0x1ffff)) {\n		off = (off + 0x20000) & ~0x1ffff;\n		blk = off >> 14;\n' + ''.join('		%s = off >> %d;\n' % (n, 13 - i) for i, n in enumerate(u)) + '	}\n'
    M.append(('m%d' % m, [(A1, new), ('	uint32_t blk;\n	int i;\n\n	blk = off', '	uint32_t blk;\n	int i;\n' + ''.join('	uint32_t %s;\n' % n for n in u) + '\n	blk = off'), (E_, ''.join('	setBeU16(off >> %d, (uint8_t *)&xb.fsReserved);\n' % (13 - i) for i in range(m)) + E_)]))
AXES = [K, M]
FLAGS = []
