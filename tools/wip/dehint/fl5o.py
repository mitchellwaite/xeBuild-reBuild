"""fl5o.py sites <label> | fl5o.py rand N seed <k> <label> [site ranges a-b,c-d]: k tests at sites within the ranges, conds and arms sampled (fl5n's)."""
import random, sys
import fllib as L, fl5lib as F, fl5f as X, fl5g as G, fl5i as I, fl5n as N

if sys.argv[1] == 'sites':
    base = X.gen(*G.parse(sys.argv[2]))
    ss = I.sites(base)
    for i, (k, ind) in enumerate(ss):
        print(i, base[k:base.find('\n', k)].strip()[:70])
else:
    n, seed, k = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    base = X.gen(*G.parse(sys.argv[5]))
    ss = I.sites(base)
    pool = []
    if len(sys.argv) > 6:
        for r in sys.argv[6].split(','):
            a, _, b = r.partition('-')
            pool += list(range(int(a), int(b or a) + 1))
    else:
        pool = list(range(len(ss)))
    rng = random.Random(seed)
    V = {}
    tries = 0
    while len(V) < n and tries < n * 30:
        tries += 1
        ps = rng.sample(pool, k)
        ts = [(rng.choice(N.CONDS[:4]), p, rng.choice((0, 1, 1, 2))) for p in ps]
        V[N.lab(sorted(ts, key=lambda t: t[1]))] = N.build(base, ss, ts)
    print(len(ss), len(V))
    F.run(V, 'o', show=10)
