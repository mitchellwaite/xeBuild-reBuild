from mv81 import *
def drop(pre, g, X):
    f = lambda evs: [e for e in evs if not ((e[0] in ('ins',) and e[2] in X) or (e[0] in ('push', 'chg', 'visit') and e[1] in X))]
    return f(pre), {b: f(v) for b, v in g.items() if b not in X}
import itertools
cands = EXTRA
res = []
for n in (1, 2, 3):
  for X in itertools.combinations(cands, n):
    for pos in (3, 9):
        p2, g2 = drop(pre, g, set(X)); g2[55] = [e for e in g2[55] if e != e81]; g2[55].insert(pos if pos == 3 else len(g2[55]) - 1, e81)
        o = srch.sim(p2, g2); res.append((pdist(o), X, pos, o))
res.sort(key=lambda r: r[0])
for r in res[:12]: print(r[0], r[1], r[2], ' '.join(map(str, r[3][r[3].index(49):])))
