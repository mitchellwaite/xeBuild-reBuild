#!/usr/bin/env python3
"""Attempt 26: op25inj2.py's any-position insert, for the extracted case (the virtual entry
is a dummy: inserted with key K at position P of a round-4 head's event group, never
visited).  Optionally remove one existing event (a block that would not be in the heap).

python tools/wip/dehint/op26inj.py REFTAG TAG -map a:b,.. -heads h1,h2 [-lo L] [-hi H]
  [-drop HEAD:IDX]  (delete event IDX of HEAD's group first)"""
import os, sys
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(H, '..', 'aio', 'p1'))
import sim3
R = os.path.join(H, '..', '..', '..', 'build', 'v', 'aio_p1')

a = sys.argv[1:]
opt = lambda k, d: a[a.index(k) + 1] if k in a else d
MAP = dict(tuple(int(y) for y in x.split(':')) for x in opt('-map', '').split(',') if x)
LO, HI = int(opt('-lo', -30)), int(opt('-hi', -1))
_, _, f3r, _, f4r = sim3.load(os.path.join(R, a[0], 'aio.bbro'))
pre, g3, f3, g4, f4 = sim3.load(os.path.join(R, a[1], 'aio.bbro'))
HEADS = [int(x) for x in opt('-heads', '').split(',') if x] or f4
V = 9001
if '-drop' in a:
    for d in opt('-drop', '').split(','):
        h, i = (int(x) for x in d.split(':'))
        print('drop', h, g4[h][i])
        del g4[h][i]


def check(g4x):
    o3, o4 = sim3.sim(pre, g3, g4x, {})
    o4 = [MAP.get(x, x) for x in o4 if x != V]
    o3 = [MAP.get(x, x) for x in o3]
    s3, s4 = set(o3), set(o4)
    return [x for x in f3r if x in s3] == o3 and [x for x in f4r if x in s4] == o4


print('base', check(g4))
n = 0
if '-r3' in a:
    # round-3 heads: the entry pushed into the next (round-4) heap at position P
    def check3(g3x):
        o3, o4 = sim3.sim(pre, g3x, g4, {})
        o4 = [MAP.get(x, x) for x in o4 if x != V]
        o3 = [MAP.get(x, x) for x in o3 if x != V]
        s3, s4 = set(o3), set(o4)
        return [x for x in f3r if x in s3] == o3 and [x for x in f4r if x in s4] == o4
    for A in f3:
        ga = g3.get(A, [])
        for p in range(len(ga) + 1):
            ks = [k for k in range(LO, HI + 1) if check3({**g3, A: ga[:p] + [('ins', 'next', V, k)] + ga[p:]})]
            if ks:
                n += 1
                print('r3 %4d @%d after %-22s keys %s' % (A, p, ga[p - 1] if p else '-', ','.join(map(str, ks))), flush=True)
    print(n, 'r3 positions with hits')
    sys.exit()
for A in HEADS:
    ga = g4.get(A, [])
    for p in range(len(ga) + 1):
        ks = [k for k in range(LO, HI + 1) if check(dict(g4, **{str(A): None}) if False else {**g4, A: ga[:p] + [('ins', 'this', V, k)] + ga[p:]})]
        if ks:
            n += 1
        print('%4d @%d after %-22s keys %s' % (A, p, ga[p - 1] if p else '-', ','.join(map(str, ks)) or '-'), flush=True)
print(n, 'positions with hits')
