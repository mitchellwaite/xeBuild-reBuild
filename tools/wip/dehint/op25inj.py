#!/usr/bin/env python3
"""Attempt 25: which extra heap operations, injected into TAG's round-4 replay (p1/sim3),
give REFTAG's extraction order.  A virtual entry V is inserted with key K at the end of
head A's event group (round 3: into the next-round heap; round 4: into this heap) and
either deleted (a 'visit') at the end of head B's group, or left to be extracted (an extra
one-block trace, what the dummies are).

python tools/wip/dehint/op25inj.py REFTAG TAG -map a:b,.. [-lo L] [-hi H] [-two]
  -ext: only the extracted case (an extra one-block trace)"""
import os, sys
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(H, '..', 'aio', 'p1'))
sys.path.insert(0, os.path.join(H, '..'))
import sim3
R = os.path.join(H, '..', '..', '..', 'build', 'v', 'aio_p1')

a = sys.argv[1:]
opt = lambda k, d: int(a[a.index(k) + 1]) if k in a else d
LO, HI = opt('-lo', -100), opt('-hi', 0)
MAP = dict(tuple(int(y) for y in x.split(':')) for x in a[a.index('-map') + 1].split(',')) if '-map' in a else {}
_, _, f3r, _, f4r = sim3.load(os.path.join(R, a[0], 'aio.bbro'))
pre, g3, f3, g4, f4 = sim3.load(os.path.join(R, a[1], 'aio.bbro'))
VS = [9001, 9002]


def check(g3x, g4x):
    o3, o4 = sim3.sim(pre, g3x, g4x, {})
    o3 = [MAP.get(x, x) for x in o3 if x not in VS]
    o4 = [MAP.get(x, x) for x in o4 if x not in VS]
    s3, s4 = set(o3), set(o4)
    return [x for x in f3r if x in s3] == o3 and [x for x in f4r if x in s4] == o4


def inject(g3x, g4x, v, k, A, rA, B):
    """copy of the groups with v inserted at A's group end (round rA), deleted at B's"""
    g3x = {h: list(e) for h, e in g3x.items()}
    g4x = {h: list(e) for h, e in g4x.items()}
    if rA == 3:
        g3x[A].append(('push', v, k))
    else:
        g4x[A].append(('ins', 'this', v, k))
    if B is not None:
        g4x[B].append(('visit', v))
    return g3x, g4x


print('base', check(g3, g4))
hits = []
for rA, heads in ((3, f3), (4, f4)):
    for ia, A in enumerate(heads):
        later = (f4 if rA == 3 else f4[ia + 1:])
        for k in range(LO, HI + 1):
            for B in ([None] if '-ext' in a else [None] + list(later)):
                gx = inject(g3, g4, VS[0], k, A, rA, B)
                if check(*gx):
                    hits.append((rA, A, k, B))
for h in hits:
    print('hit r%d after %s key %d %s' % (h[0], h[1], h[2], 'extracted' if h[3] is None else 'deleted after %s' % h[3]))
print(len(hits), 'single-injection hits')
