"""fl4k.py N seed [p]: random dead-test subsets and arm sizes at fl4f's base (p = probability a site has a test)."""
import random, sys
import fllib as L, fl4lib as F, fl4d as D, fl4f as B, fl4g as G
N, seed = int(sys.argv[1]), int(sys.argv[2])
p = float(sys.argv[3]) if len(sys.argv) > 3 else 0.4
rng = random.Random(seed)
V = {}
while len(V) < N:
    parts = []
    for n in F.SITES:
        if rng.random() < p:
            parts.append('%s=%d' % (n, rng.choice((1, 1, 1, 2, 2, 3, 4, 5))))
    l = ','.join(parts)
    if l not in V:
        V[l] = G.mk(F.st(l))
print(len(V))
F.run(V, 'k', show=25)
