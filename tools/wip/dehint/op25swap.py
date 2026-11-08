#!/usr/bin/env python3
"""Attempt 25: swaps of two inserts inside one head's event group (the order a trace pushes
a block's unvisited successors: the succ edge order, which arm order in the source sets),
singly and in pairs, in TAG's replay against REFTAG's order.  Also the pre-round-3 events
(rounds 1-2 pushes into later heaps) per trace.

python tools/wip/dehint/op25swap.py REFTAG TAG -map a:b,.. [-2]"""
import itertools, os, sys
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(H, '..', 'aio', 'p1'))
sys.path.insert(0, os.path.join(H, '..'))
import sim3
R = os.path.join(H, '..', '..', '..', 'build', 'v', 'aio_p1')

a = sys.argv[1:]
MAP = dict(tuple(int(y) for y in x.split(':')) for x in a[a.index('-map') + 1].split(','))
DROP = set(int(x) for x in a[a.index('-drop') + 1].split(',')) if '-drop' in a else set()
_, _, f3r, _, f4r = sim3.load(os.path.join(R, a[0], 'aio.bbro'))
pre, g3, f3, g4, f4 = sim3.load(os.path.join(R, a[1], 'aio.bbro'))


def check(prex, g3x, g4x):
    o3, o4 = sim3.sim(prex, g3x, g4x, {})
    o3 = [MAP.get(x, x) for x in o3 if x not in DROP]
    o4 = [MAP.get(x, x) for x in o4 if x not in DROP]
    s3, s4 = set(o3), set(o4)
    return [x for x in f3r if x in s3] == o3 and [x for x in f4r if x in s4] == o4


# candidate swaps: (where, key, i, j) with i<j both inserts in the same group and no 'get'
# between them (pre: between two gets)
cands = []
gi = [i for i, e in enumerate(pre) if e[0] in ('get', 'round')] + [len(pre)]
for s, t in zip(gi, gi[1:]):
    ins = [i for i in range(s, t) if pre[i][0] in ('ins', 'push')]
    for i, j in itertools.combinations(ins, 2):
        cands.append(('pre', None, i, j))
for nm, g in (('g3', g3), ('g4', g4)):
    for h, evs in g.items():
        ins = [i for i, e in enumerate(evs) if e[0] in ('ins', 'push')]
        for i, j in itertools.combinations(ins, 2):
            cands.append((nm, h, i, j))
print(len(cands), 'candidate swaps', flush=True)


def applied(cs):
    prex = list(pre)
    g3x = {k: list(v) for k, v in g3.items()}
    g4x = {k: list(v) for k, v in g4.items()}
    for nm, h, i, j in cs:
        L = prex if nm == 'pre' else (g3x if nm == 'g3' else g4x)[h]
        L[i], L[j] = L[j], L[i]
    return prex, g3x, g4x


def show(c):
    nm, h, i, j = c
    L = pre if nm == 'pre' else (g3 if nm == 'g3' else g4)[h]
    return '%s %s: %s <-> %s' % (nm, h, L[i], L[j])


n = 0
for c in cands:
    if check(*applied([c])):
        n += 1
        print('hit', show(c), flush=True)
print(n, 'single hits', flush=True)
if '-2' in a:
    m = 0
    for c1, c2 in itertools.combinations(cands, 2):
        if c1[:2] == c2[:2] and set(c1[2:]) & set(c2[2:]):
            continue
        if check(*applied([c1, c2])):
            m += 1
            print('hit2', show(c1), '|', show(c2), flush=True)
    print(m, 'pair hits')
