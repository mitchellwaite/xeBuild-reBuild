# attempt 15, probe only (never a candidate): K extra SSA names released at VRP1 from a dead arm, at each position in writeFsTable, on a14 (IWB= other base).
# Tests the reading that the big copy's compare depends on how many names sit above ccp2's layer of the free list.
import os
BASE = os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_a14.c')
POS = ['	buf = malloc(0x4000);\n', '	log_printf(1, "offset 0x%x len 0x4000', '	if (!xb.bigBlock)\n		goto small;\n']
OPS = ['z += 1;', 'z ^= 3;', 'z <<= 2;', 'z -= 7;', 'z |= 9;', 'z >>= 1;', 'z *= 5;', 'z &= 0xfff;', 'z += off;', 'z ^= off;']
A = [('', [])]
for pi, ps in enumerate(POS):
    for k in range(0, 11):
        A.append(('p%dk%d' % (pi, k), [(ps, '	if ((off & 0x3fff) > 0x3fff) {\n		uint32_t z = off;\n		%s\n		off = z;\n	}\n' % ' '.join(OPS[:k]) + ps)]))
AXES = [A]
FLAGS = []
