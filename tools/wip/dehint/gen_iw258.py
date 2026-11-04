# attempt 18, probe only (dead arms aren't candidates): pin_hdr. Without the pin spare gets eax because hdr's pretmp has the lower version (src: spare 300, hdr 295; gen_iw255 `hl`: hdr 300, spare 298, hdr gets eax). The reference loads spare first, so the wanted pops are ascending, spare low then hdr high: a boundary of the free list between them. K names freed by a dead arm in finalizeImage move that window.
# `IWB=build/iw/a18/noph.c python tools/wip/dehint/iw16sweep.py tools/wip/dehint/gen_iw258.py -n 12 -t 1`
import os
BASE = os.environ.get('IWB', 'build/iw/a18/noph.c')
ps = '	log_printf(1, "calculating ECD bytes and assembling raw image...");\n'
OPS = ['z += 1;', 'z ^= 3;', 'z <<= 2;', 'z -= 7;', 'z |= 9;', 'z >>= 1;', 'z *= 5;', 'z &= 0xfff;', 'z += n;', 'z ^= n;']
A = []
for k in range(0, 61):
    b = ' '.join(OPS[j % 10] for j in range(k))
    A.append(('k%d' % k, [(ps, '	if ((n & 0xff) > 0x100 - 1 + (b = 0)) {\n		uint32_t z = n;\n		%s\n		n = z;\n	}\n' % b + ps)]))
AXES = [A]
FLAGS = []
