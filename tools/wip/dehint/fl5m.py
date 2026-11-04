"""fl5m.py <fl5f label> <k> <N> <seed>: k extra dead tests at random statement sites of an fl5f state, N samples.
Site clusters: conds off < -1, off < 0, pos < 0, size < 0; one or two stores."""
import random, sys
import fllib as L, fl5lib as F, fl5f as X, fl5g as G, fl5i as I

base = X.gen(*G.parse(sys.argv[1]))
k, N, seed = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
ss = I.sites(base)
rng = random.Random(seed)
V = {}
while len(V) < N:
    ps = sorted(rng.sample(range(len(ss)), k), reverse=True)
    s = base
    lab = []
    for p in ps:
        c = rng.choice(I.CONDS)
        a = rng.choice(I.ARMS)
        s = I.ins(s, ss[p][0], ss[p][1], c, a)
        lab.append('%s@%d/%d' % (c, p, I.ARMS.index(a)))
    V[' '.join(lab)] = s
print(len(ss), len(V))
F.run(V, 'm', show=10)
