"""fl5p.py <fl5f label> '<tests>' [N seed]: fl5c's axes (each alone, then N random pairs and triples among those that aren't transparent) and fl5f's other axes on a state with extra dead tests."""
import random, sys
import fllib as L, fl5lib as F, fl5f as X, fl5g as G, fl5i as I, fl5n as N, fl5c as C

lb = sys.argv[1]
fc, t = G.parse(lb)
ts = N.parse(sys.argv[2])


def mk(fc2, cc):
    base = X.gen(fc, t)
    ss = I.sites(base)
    s = N.build(base, ss, ts)
    for a in C.ORDER:
        if a in cc:
            if a == 'base' and 'tool' in cc:
                continue
            s = C.AX[a][cc[a]](s)
    return s


V = {}
for a in C.ORDER:
    for v in C.AX[a]:
        try:
            V['%s=%s' % (a, v)] = mk(fc, {a: v})
        except (ValueError, AttributeError, AssertionError):
            pass
R = F.run(V, 'p', show=12)
base = F.one(('b', mk(fc, {})))[0]
live = [r[3] for r in R if r[0] != base and r[0] < 60]
print(base, live)
if len(sys.argv) > 3:
    n, seed = int(sys.argv[3]), int(sys.argv[4])
    rng = random.Random(seed)
    W = {}
    tries = 0
    while len(W) < n and tries < 30 * n:
        tries += 1
        pick = rng.sample(live, min(rng.choice((2, 2, 3, 4)), len(live)))
        cc = dict(p.split('=') for p in pick)
        try:
            W[','.join(pick)] = mk(fc, cc)
        except (ValueError, AttributeError, AssertionError):
            pass
    print(len(W))
    F.run(W, 'p', show=12)
