#!/usr/bin/env python3
"""Attempt 25: op25inj.py with the virtual entry's insert and delete at any position inside
round-4 event groups (not only group ends), for a set of keys.

python tools/wip/dehint/op25inj2.py REFTAG TAG -map a:b,.. -keys k1,k2,.. [-heads h1,h2,..]"""
import os, sys
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(H, '..', 'aio', 'p1'))
sys.path.insert(0, os.path.join(H, '..'))
import sim3
R = os.path.join(H, '..', '..', '..', 'build', 'v', 'aio_p1')

a = sys.argv[1:]
MAP = dict(tuple(int(y) for y in x.split(':')) for x in a[a.index('-map') + 1].split(','))
KEYS = [int(x) for x in a[a.index('-keys') + 1].split(',')]
_, _, f3r, _, f4r = sim3.load(os.path.join(R, a[0], 'aio.bbro'))
pre, g3, f3, g4, f4 = sim3.load(os.path.join(R, a[1], 'aio.bbro'))
HEADS = [int(x) for x in a[a.index('-heads') + 1].split(',')] if '-heads' in a else f4
V = 9001


def check(g4x):
    o3, o4 = sim3.sim(pre, g3, g4x, {})
    o4 = [MAP.get(x, x) for x in o4 if x != V]
    o3 = [MAP.get(x, x) for x in o3]
    s3, s4 = set(o3), set(o4)
    return [x for x in f3r if x in s3] == o3 and [x for x in f4r if x in s4] == o4


n = 0
for ia, A in enumerate(f4):
    if A not in HEADS:
        continue
    ga = g4.get(A, [])
    for pa in range(len(ga) + 1):
        for k in KEYS:
            for ib in range(ia, len(f4)):
                B = f4[ib]
                gb0 = g4.get(B, [])
                for pb in range(len(gb0) + 1):
                    if ib == ia and pb <= pa:
                        continue
                    g = {h: list(e) for h, e in g4.items()}
                    g.setdefault(A, [])
                    g[A].insert(pa, ('ins', 'this', V, k))
                    g.setdefault(B, [])
                    q = pb + (1 if B == A else 0)
                    g[B].insert(q, ('visit', V))
                    if check(g):
                        n += 1
                        print('hit ins %s@%d (%s) key %d  del %s@%d (%s)' % (A, pa, ga[pa - 1] if pa else '-', k, B, pb, gb0[pb - 1] if pb else '-'), flush=True)
print(n, 'hits')
