# sa.py SEED CHAIN INITCFG(json) STEPS : simulated annealing over lev.py cfg; cost f2 + 0.1*dist
import sys, json, random, math, subprocess, os, lev
sys.path.insert(0, '../s104'); import srch
seed, ch, init, steps = int(sys.argv[1]), sys.argv[2], json.loads(sys.argv[3]), int(sys.argv[4])
random.seed(seed); d = 'sa_' + ch; os.makedirs(d, exist_ok=True)
SPACE = dict(wb3=['b', '2', '1', 'n'], wb4=[0, 1, 2, 3, 4], c11=[3, 4, 5], k=[0, 1, 2], e=[0, 1],
             pf=list(range(-1, 8)), pfn=[1, 2, 3], ps=list(range(-1, 8)), psn=[1, 2, 3],
             po=list(range(-1, 8)), pv=list(range(-1, 8)))
cache = {}
def ev(cfg):
    n = lev.name(cfg)
    if n in cache: return cache[n]
    p = '%s/v_%s.c' % (d, n)
    try: open(p, 'w', newline='\n').write(lev.apply(cfg))
    except AssertionError: cache[n] = (9999, 99, ''); return cache[n]
    out = subprocess.run(['sh', '../s104/run.sh', p], capture_output=True, text=True).stdout.split()
    try: f = int(out[1].split('=')[1]); o = list(map(int, out[3:])); di = srch.dist(o)
    except Exception: f, di = 9999, 99
    cache[n] = (f, di, n); print('%s f2=%d d=%d' % (n, f, di), flush=True); return cache[n]
cost = lambda r: r[0] + 0.1 * r[1]
cur = dict(init); rc = ev(cur); best = (rc, dict(cur))
for t in range(steps):
    T = 8.0 * (1 - t / steps) + 0.5
    nw = dict(cur)
    for _ in range(random.choice([1, 1, 2])):
        k = random.choice(list(SPACE)); nw[k] = random.choice(SPACE[k])
    r = ev(nw)
    if cost(r) <= cost(rc) or random.random() < math.exp((cost(rc) - cost(r)) / T):
        cur, rc = nw, r
        if cost(r) < cost(best[0]): best = (r, dict(nw)); print('BEST', r, json.dumps(nw), flush=True)
print('FINAL', best[0], json.dumps(best[1]))
