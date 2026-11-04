"""python tools/wip/dehint/iw12probe.py <base.c> [probe ...]: PROBES ONLY, never candidates: expect + param grid on one branch at a time, to see how far each branch's probability is from flipping imgAddFile's slots 0x30/0x34.  Prints per-function lines per probability."""
import os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib

P = {
 'big': ('		if (!xb.bigBlock)\n			imgAdd(off, data, len, 0, 0xffff, 1);', '		if (__builtin_expect(!xb.bigBlock, 0))\n			imgAdd(off, data, len, 0, 0xffff, 1);'),
 'fits': ('	if (imgFits(off, len)) {\n		fsFiles[nFsFiles].block', '	if (__builtin_expect(imgFits(off, len), 1)) {\n		fsFiles[nFsFiles].block'),
 'raw1': ('	if (xb.rawSize < off || xb.rawSize < off + len) {\n		return -1;\n	}\n	x = off & 0x3fff;', '	if (__builtin_expect(xb.rawSize < off || xb.rawSize < off + len, 0)) {\n		return -1;\n	}\n	x = off & 0x3fff;'),
 'outer': ('	for (b = 0; b < blocks; b++) {\n		/* blk', '	for (b = 0; __builtin_expect(b < blocks, 1); b++) {\n		/* blk'),
 'inner': ('		for (end = p + npages; p < end; p++) {\n			/* a statement', '		for (end = p + npages; __builtin_expect(p < end, 0); p++) {\n			/* a statement'),
 'partial': ('		if (partial) {\n', '		if (__builtin_expect(partial, 1)) {\n'),
 'aligned': None,
}
t = open(sys.argv[1], newline='').read().replace('\r\n', '\n')
names = sys.argv[2:] or [k for k in P if P[k]]
GRID = [52,54,55,56,57,58,60,61,62,64,65,67,70,73,75,78,80,85,89,90]


def one(a):
    n, p = a
    x, y = P[n]
    if x not in t:
        return n, p, 'edit not found'
    r = iwlib.score_text(t.replace(x, y), ['--param', 'builtin-expect-probability=%d' % p])
    return n, p, r.get('per')


with ThreadPoolExecutor(4) as ex:
    for n, p, per in ex.map(one, [(n, p) for n in names for p in GRID]):
        print(n, p, per)
