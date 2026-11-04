"""fl4p.py N seed [p]: random dead tests (p) x random near-transparent helpers, at fl4f's base."""
import random, sys
import fllib as L, fl4lib as F, fl4g as G, fl4m as M
N, seed = int(sys.argv[1]), int(sys.argv[2])
p = float(sys.argv[3]) if len(sys.argv) > 3 else 0.3
AXN = ['strip', 'sect', 'out', 'pre', 'flen', 'hex', 'ks']
rng = random.Random(seed)
V = {}
while len(V) < N:
    parts = []
    for n in F.SITES:
        if rng.random() < p:
            parts.append('%s=%d' % (n, rng.choice((1, 1, 1, 2, 2, 3))))
    tl = ','.join(parts)
    c = {}
    for a in AXN:
        if rng.random() < 0.25:
            v = rng.choice(list(M.AX[a]))
            if a == 'flen' and 'r' in v:
                continue
            c[a] = v
    l = tl + '|' + M.lab(c)
    if l not in V:
        V[l] = M.gen(c, G.mk(F.st(tl)))
print(len(V))
F.run(V, 'p', show=25)
