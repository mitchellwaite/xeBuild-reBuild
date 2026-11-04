"""fl5q.py <k> [N seed]: with hsec=cn and each of the live shifts (pre, fail, out and pairs), fewer tests than the 5 -> 4 match:
k=1: off4 plus one test anywhere; k=0 scan; k=2: no off4, two tests sampled."""
import random, sys
import fllib as L, fl5lib as F, fl5f as X, fl5i as I, fl5n as N, fl5c as C

SHIFTS = [{}, {'pre': 'y'}, {'fail': 'y'}, {'out': 'y'}, {'pre': 'y', 'out': 'y'}, {'fail': 'y', 'out': 'y'}]


def mk(t, ts, cc):
    base = X.gen({'hsec': 'cn'}, t)
    ss = I.sites(base)
    s = N.build(base, ss, ts)
    for a, v in cc.items():
        s = C.AX[a][v](s)
    return s


k = int(sys.argv[1])
V = {}
if k == 0:
    for cc in SHIFTS:
        for t in [(), ('off4',), ('off3', 'off4'), ('off4', 'x'), ('raw', 'off4')]:
            V['%s|%s' % (','.join(cc), '+'.join(t))] = mk(t, [], cc)
elif k == 1:
    n = len(I.sites(X.gen({'hsec': 'cn'}, ('off4',))))
    for cc in SHIFTS[1:3]:
        for p in range(n):
            for c in ('off < -1', 'off < 0'):
                for a in (0, 1):
                    V['%s|off4 %s@%d/%d' % (','.join(cc), c, p, a)] = mk(('off4',), [(c, p, a)], cc)
else:
    N_, seed = int(sys.argv[2]), int(sys.argv[3])
    rng = random.Random(seed)
    n = len(I.sites(X.gen({'hsec': 'cn'}, ())))
    while len(V) < N_:
        cc = rng.choice(SHIFTS[1:3])
        ps = rng.sample(range(n), 2)
        ts = [(rng.choice(('off < -1', 'off < 0')), p, rng.choice((0, 1))) for p in ps]
        V['%s| %s' % (','.join(cc), N.lab(ts))] = mk((), ts, cc)
print(len(V))
F.run(V, 'q', show=12)
