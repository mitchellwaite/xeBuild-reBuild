#!/usr/bin/env python3
"""Attempt 25: single mutations of TAG's heap event list (p1/sim3 replay) that give REFTAG's
extraction order: drop one round-3/4 insert (with every later op on that entry), or move one
insert to another position (round 3 pushes and round 4 inserts).

python tools/wip/dehint/op25mut.py REFTAG TAG -map a:b,.. [drop|move]"""
import os, sys
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(H, '..', 'aio', 'p1'))
sys.path.insert(0, os.path.join(H, '..'))
import sim3
R = os.path.join(H, '..', '..', '..', 'build', 'v', 'aio_p1')

a = sys.argv[1:]
MAP = dict(tuple(int(y) for y in x.split(':')) for x in a[a.index('-map') + 1].split(','))
_, _, f3r, _, f4r = sim3.load(os.path.join(R, a[0], 'aio.bbro'))
pre, g3, f3, g4, f4 = sim3.load(os.path.join(R, a[1], 'aio.bbro'))


def check(g3x, g4x, drop=()):
    o3, o4 = sim3.sim(pre, g3x, g4x, {})
    o3 = [MAP.get(x, x) for x in o3 if x not in drop]
    o4 = [MAP.get(x, x) for x in o4 if x not in drop]
    s3, s4 = set(o3), set(o4)
    return [x for x in f3r if x in s3] == o3 and [x for x in f4r if x in s4] == o4


def ent(e):
    return e[2] if e[0] == 'ins' else e[1]


slots = [(3, h, i) for h in f3 for i in range(len(g3.get(h, [])))] + \
        [(4, h, i) for h in f4 for i in range(len(g4.get(h, [])))]
mode = 'move' if 'move' in a else 'drop'
n = 0
for r, h, i in slots:
    g = g3 if r == 3 else g4
    e = g[h][i]
    if e[0] not in ('ins', 'push'):
        continue
    if mode == 'drop':
        g3x = {k: list(v) for k, v in g3.items()}
        g4x = {k: list(v) for k, v in g4.items()}
        (g3x if r == 3 else g4x)[h].pop(i)
        if check(g3x, g4x):
            n += 1
            print('drop r%d %s@%d %s' % (r, h, i, e), flush=True)
        continue
    # move: take the op out and put it at the end of another head's group (same round kind)
    for r2, heads in ((3, f3), (4, f4)):
        for h2 in heads:
            for j in range(len((g3 if r2 == 3 else g4).get(h2, [])) + 1):
                g3x = {k: list(v) for k, v in g3.items()}
                g4x = {k: list(v) for k, v in g4.items()}
                (g3x if r == 3 else g4x)[h].pop(i)
                e2 = e
                if r2 == 3 and e[0] == 'ins':
                    e2 = ('push', e[2], e[3]) if e[1] == 'next' else ('ins', 'this', e[2], e[3])
                if r2 == 4 and e[0] == 'push':
                    e2 = ('ins', 'this', e[1], e[2])
                gg = g3x if r2 == 3 else g4x
                gg.setdefault(h2, []).insert(j, e2)
                if (r2, h2, j) == (r, h, i):
                    continue
                if check(g3x, g4x):
                    n += 1
                    print('move %s from r%d %s@%d to r%d %s@%d' % (e, r, h, i, r2, h2, j), flush=True)
print(n, 'hits')
