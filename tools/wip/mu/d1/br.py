"""br.py DUMP [pairs]: brute force single (and pair) key overrides on the exact heap model, no dummies.  Prints those giving the target order (FLEX free)."""
import itertools
import sys

import dsim

M = dsim.load(sys.argv[1])
o3, o4 = dsim.sim(M)
print('r3 same', o3 == M['f3'], 'r4 same', o4 == M['f4'], 'start', dsim.score(o4))
W = dsim.WANT
ev = M['g4']
keys = {}
for g in list(M['g3'].values()) + list(M['g4'].values()) + [M['pre']]:
    for e in g:
        if e[0] == 'ins':
            keys[e[2]] = e[3]
        elif e[0] == 'push':
            keys[e[1]] = e[2]
nodes = o4
print('r4 base keys', {b: keys.get(b) for b in nodes})


def good(ov):
    try:
        _, o = dsim.sim(M, ov)
    except Exception:
        return False
    return [b for b in o if b not in dsim.FLEX] == W


sing = []
for b in nodes:
    for k in range(-10, 1):
        if k == keys.get(b):
            continue
        if good({b: k}):
            sing.append((b, k))
print('singles', [(b, k, keys.get(b)) for b, k in sing])
if len(sys.argv) > 2:
    n = 0
    for a, b in itertools.combinations(nodes, 2):
        for ka in range(keys[a] - 2, min(keys[a] + 3, 1)):
            for kb in range(keys[b] - 2, min(keys[b] + 3, 1)):
                if ka == keys[a] or kb == keys[b]:
                    continue
                if good({a: ka, b: kb}):
                    print('pair', a, ka, keys[a], b, kb, keys[b])
                    n += 1
    print('pairs', n)
