"""fl5d.py N seed T: combinations of the axes that aren't transparent (score differs from the bare state alone) at test subset T ('-' for none)."""
import random, sys
import fllib as L, fl5lib as F, fl5c as C

t = () if sys.argv[3] == '-' else tuple(sys.argv[3].split(','))
base = F.one(('b', F.gen(t)))[0]
V = {}
for a in C.ORDER:
    for v in C.AX[a]:
        try:
            V[(a, v)] = C.gen({a: v}, t)
        except (ValueError, AttributeError, AssertionError):
            pass
S = F.run({'%s=%s' % k: s for k, s in V.items()}, 'd1', show=0)
live = [tuple(r[3].split('=')) for r in S if r[0] != base and r[0] < 700]
print(base, len(V), 'live', [(r[3], r[0]) for r in S if r[0] != base and r[0] < 700])
N, seed = int(sys.argv[1]), int(sys.argv[2])
rng = random.Random(seed)
W = {}
tries = 0
while len(W) < N and tries < N * 20:
    tries += 1
    k = rng.choice((2, 2, 3, 3, 4, 5))
    c = {}
    for a, v in rng.sample(live, min(k, len(live))):
        c[a] = v
    try:
        W[C.lab(c, t)] = C.gen(c, t)
    except (ValueError, AttributeError, AssertionError):
        pass
print(len(W))
F.run(W, 'd', show=14)
