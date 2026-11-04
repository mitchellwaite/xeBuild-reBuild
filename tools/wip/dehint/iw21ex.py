"""attempt 21: mechanism probe, not a candidate. imgAddFile's `_45` v npages slot order at P(partial) 50: _45's entry reference is the only one outside the inlined imgAdd, so lower the entry's frequency relative to it with expect on the bigBlock test.
python tools/wip/dehint/iw21ex.py <base.c>"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib
from concurrent.futures import ThreadPoolExecutor
t = open(sys.argv[1], newline='').read().replace('\r\n', '\n')
K = 'if (!xb.bigBlock)\n\t\t\timgAdd(off, data, len, 0, 0xffff, 1);'
assert K in t
def one(a):
    v, n = a
    t2 = t.replace(K, K.replace('!xb.bigBlock', '__builtin_expect(!xb.bigBlock, %d)' % v))
    return v, n, iwlib.fmt(iwlib.score_text(t2, ['--param', 'builtin-expect-probability=%d' % n]))[:150]
for r in ThreadPoolExecutor(4).map(one, [(v, n) for v in (0, 1) for n in (52, 55, 56, 58, 60, 62, 65, 68, 71, 73, 75, 80)]):
    print(r)
