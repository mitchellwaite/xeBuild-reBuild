import sys, random, itertools
from r4sim import load, sim
pre, g, first = load(sys.argv[1])
T = [int(x) for x in sys.argv[2].split(',')]
S = [int(x) for x in sys.argv[3].split(',')]
vals = [0, -1, -2, -3, -4]
def cost(o):
    p = [b for b in o if b in T]
    # number of inversions vs T
    pos = {b: i for i, b in enumerate(T)}
    q = [pos[b] for b in p]
    return sum(1 for i in range(len(q)) for j in range(i+1, len(q)) if q[i] > q[j])
base = cost(sim(pre, g, {}))
print('base', base)
res = []
for n in (1, 2):
    for bs in itertools.combinations(S, n):
        for ks in itertools.product(vals, repeat=n):
            ov = dict(zip(bs, ks))
            c = cost(sim(pre, g, ov))
            res.append((c, n, ov))
res.sort(key=lambda r: (r[0], r[1]))
for r in res[:25]: print(r)
