"""pk.py DUMP: search priority-form keys.  key = -(1000000 + 100*e + f) where e = edge freq from a trace end, f = bb freq (see bb_to_key).
Prints, per priority block, the (e,f) overrides reaching the target order on the exact heap model, then the same for plain (non-priority) keys,
then pairs among 43/44/105/128."""
import itertools
import sys

import dsim

M = dsim.load(sys.argv[1])


def score(ov):
    _, o = dsim.sim(M, ov)
    o = [b for b in o if b not in dsim.FLEX]
    pos = {b: i for i, b in enumerate(dsim.WANT)}
    x = [pos[b] for b in o if b in pos]
    return sum(1 for i in range(len(x)) for j in range(i + 1, len(x)) if x[i] > x[j])


def P(e, f):
    return -(1000000 + 100 * e + f)


print('base inversions', score({}))
pri = {}
for g in list(M['g3'].values()) + list(M['g4'].values()) + [M['pre']]:
    for ev in g:
        if ev[0] == 'chg':
            pri[ev[1]] = ev[2]
print('priority blocks', pri)
for b, k in pri.items():
    z = [(e, f) for e in range(0, 16) for f in range(0, 16) if score({b: P(e, f)}) == 0]
    if z:
        print(b, 'valid', sorted(set(e for e, f in z)), 'f', sorted(set(f for e, f in z)), len(z))
print('pairs (e only, f = 9 for 43/44/105, 6 for 128)')
BF = {43: 9, 44: 9, 105: 9, 128: 6}
for a, b in itertools.combinations(BF, 2):
    z = [(ea, eb) for ea in range(3, 16) for eb in range(3, 16) if score({a: P(ea, BF[a]), b: P(eb, BF[b])}) == 0]
    print(a, b, z[:30])
print('105 e/f, 128 e/f with fine f')
z = [(e5, f5, e8, f8) for e5 in range(5, 12) for f5 in range(6, 12) for e8 in range(3, 12) for f8 in range(3, 10)
     if score({105: P(e5, f5), 128: P(e8, f8)}) == 0]
print(len(z), z[:60])
