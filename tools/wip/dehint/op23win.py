"""Attempt 23: key windows of chosen blocks in TAG's bbro heap replay (op16sim), one block
at a time, the rest as dumped.

python tools/wip/dehint/op23win.py REFTAG TAG b1,b2,.. LO HI"""
import os, sys
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
import op16sim

a = sys.argv[1:]
refd, tagd = op16sim.load(a[0]), op16sim.load(a[1])
lo, hi = int(a[3]), int(a[4])
ks = op16sim.keys_of(tagd[0], tagd[1], tagd[3])
for b in [int(x) for x in a[2].split(',')]:
    hits = [k for k in range(lo, hi + 1) if op16sim.compare(refd, tagd, {b: k}, {})[0]]
    print('block', b, 'keys', ks.get(b), 'hits', (hits if len(hits) < 20 else '%d..%d (%d)' % (hits[0], hits[-1], len(hits))))
