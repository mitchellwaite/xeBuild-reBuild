"""fl8v.py N [seed]: attempt 6's natural helper axes (fl6lib.E) in combination with the conversions of fl8e (which attempt 6 didn't have), at the drop states closest to matching."""
import random, sys
import fllib as L, fl6lib as F, fl8lib as T
import fl8e as X

CONV = ['', '', 'pre_u', 'gfs_u', 'pre_u+gfs_u', 'fs_fr1', 'fs_uint32_t', 'fs_uint32_t+gfs_u', 'fs_fr1+gfs_u', 'fs_fr1+pre_u']
AXES = [a for a in F.ORDER if a != 'pre']
DROPS = ['T1,T3', 'T1,T2,T3', 'T3', 'T1,T2', 'T1']


def build(d, ax, conv):
    s = F.drop(T.S0, [x for x in d.split(',') if x])
    for a in AXES:
        if a in ax:
            s = F.E[a][ax[a]](s)
    if conv:
        for c in conv.split('+'):
            s = X.ALL[c](s)
    return s


N = int(sys.argv[1])
random.seed(int(sys.argv[2]) if len(sys.argv) > 2 else 1)
V = {}
tries = 0
while len(V) < N and tries < N * 5:
    tries += 1
    d = random.choice(DROPS)
    ax = {}
    for a in random.sample(AXES, random.choice([1, 1, 2, 2, 3])):
        ax[a] = random.choice(list(F.E[a]))
    if 'adv' in ax and 'copy' in ax:
        continue
    conv = random.choice(CONV)
    lb = '%s|%s|%s' % (d, ','.join('%s=%s' % kv for kv in sorted(ax.items())), conv)
    if lb in V:
        continue
    try:
        V[lb] = build(d, ax, conv)
    except ValueError:
        continue
print(len(V))
rs = T.run(V, 'v', 0)
for r in rs[:15]:
    print(r[0], r[1], r[3])
T.floors(rs)
