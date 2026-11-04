"""fl4s.py N seed k: k dead tests at random statement sites (fl4r's) from fl4f's base; the seven old sites excluded.
Also, first, all subsets of the old sites with site 62 at arms 1-2."""
import itertools, random, sys
import fllib as L, fl4lib as F, fl4g as G, fl4r as R

N, seed, K = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
V = {}
base = G.mk({})
ss = R.sites(base)
rng = random.Random(seed)
for r in range(0, 4):
    for c in itertools.combinations(['off3', 'off4', 'x', 'i', 'nul'], r):
        for ks in itertools.product((1, 2), repeat=r):
            tl = ','.join('%s=%d' % z for z in zip(c, ks))
            s = G.mk(F.st(tl))
            sx = R.sites(s)
            # the same statement: the site index shifts with tests above it, so find it by text
            V['sub ' + tl] = s
while len(V) < N:
    ps = sorted(rng.sample(range(len(ss)), K), reverse=True)
    cs = [rng.choice(R.CONDS[:3]) for _ in ps]
    s = base
    for p, c in zip(ps, cs):
        s = R.ins(s, ss[p][0], ss[p][1], c, '*buf = 0')
    V[' '.join('%s@%d' % z for z in zip(cs, ps))] = s
print(len(V))
F.run(V, 's', show=14)
