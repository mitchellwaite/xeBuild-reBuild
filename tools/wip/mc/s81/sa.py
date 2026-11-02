import sys, random
from r4sim import load, sim
pre, g, first = load(sys.argv[1])
T = [int(x) for x in sys.argv[2].split(',')]
S = [int(x) for x in sys.argv[3].split(',')]
vals = [None, 0, -1, -2, -3, -4]
pos = {b: i for i, b in enumerate(T)}
def cost(ov):
    o = sim(pre, g, {k: v for k, v in ov.items() if v is not None})
    q = [pos[b] for b in o if b in pos]
    inv = sum(1 for i in range(len(q)) for j in range(i+1, len(q)) if q[i] > q[j])
    return inv * 10 + sum(1 for v in ov.values() if v is not None)
best = None
for rep in range(int(sys.argv[4]) if len(sys.argv) > 4 else 6):
    random.seed(rep); ov = {b: None for b in S}; c = cost(ov); t = 20.0
    for it in range(3000):
        b = random.choice(S); old = ov[b]; ov[b] = random.choice(vals)
        c2 = cost(ov)
        if c2 <= c or random.random() < pow(2.718, (c - c2) / t): c = c2
        else: ov[b] = old
        t *= 0.998
    if best is None or c < best[0]: best = (c, dict(ov))
    print(rep, c, {k: v for k, v in ov.items() if v is not None}, flush=True)
print('best', best[0], {k: v for k, v in best[1].items() if v is not None})
