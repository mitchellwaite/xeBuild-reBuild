"""anneal.py EVALS SEED [T0]: simulated annealing over the fake7 design space (same env as fake7).
Moves: 1-4 random +-1/+-2 changes on f/P vars.  Prints improvements and the final best."""
import os, sys, json, random, math
EV, SEED = int(sys.argv[1]), int(sys.argv[2]); T0 = float(sys.argv[3]) if len(sys.argv) > 3 else 1.5
sys.argv = ['x', '0', '1']
import fake7
random.seed(SEED)
KEYS = [('f', k) for k in fake7.FK] + [('P', k) for k in fake7.PK]
def lim(b):
    return (-1, 1) if b == 'd49' else (0, fake7.VMAX - 1)
def val(c):
    return fake7.val(c[0], c[1])
cur = (dict(fake7.BASE), dict(fake7.BP)); cs = val(cur)
best, bs = cur, cs
print('start', cs, flush=True)
for i in range(EV):
    T = T0 * (1 - i / EV) + 0.05
    f, P = dict(cur[0]), dict(cur[1])
    for _ in range(random.choice((1, 1, 2, 2, 3, 4))):
        kind, b = random.choice(KEYS); d = f if kind == 'f' else P
        lo, hi = lim(b)
        d[b] = max(lo, min(hi, d.get(b, 0) + random.choice((-1, 1, -1, 1, -2, 2))))
    x = val((f, P))
    if x >= 998: continue
    if x <= cs or random.random() < math.exp((cs - x) / T):
        cur, cs = (f, P), x
        if x < bs:
            best, bs = (dict(f), dict(P)), x; print(i, bs, flush=True)
            if bs == 0: break
print('best', bs, json.dumps({'f': best[0], 'P': best[1]}))
PP = dict(best[1]); fake7.ok(best[0], PP)
print(' '.join(map(str, fake7.sim(best[0], PP))))
