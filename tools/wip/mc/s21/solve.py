"""solve.py TABLE.json DESIGN.json [ITERS] [MAXN]: additive-model anneal over injection subsets
(rows of table.py) minimising L1(basefq + sum d - design); rows with missing blocks excluded.
Prints chosen injections (json) and predicted dist."""
import json, random, sys, math
T = json.load(open(sys.argv[1])); des = {int(k): v for k, v in json.load(open(sys.argv[2])).items()}
IT = int(sys.argv[3]) if len(sys.argv) > 3 else 200000; MAXN = int(sys.argv[4]) if len(sys.argv) > 4 else 12
base = {int(k): v for k, v in T['basefq'].items()}
rows = [r for r in T['rows'] if not r['miss'] and r['d']]
# dedupe identical delta vectors
seen = {}; 
for r in rows:
    k = json.dumps(sorted(r['d'].items()))
    if k not in seen or r['inv'] < seen[k]['inv']: seen[k] = r
rows = list(seen.values()); print(len(rows), 'distinct rows', file=sys.stderr)
D = [{int(k): v for k, v in r['d'].items()} for r in rows]
def dist(sel):
    f = dict(base)
    for i in sel:
        for k, v in D[i].items(): f[k] = f.get(k, 0) + v
    return sum(abs(f.get(b, 0) - v) for b, v in des.items()) + sum(abs(v - base.get(k, 0)) for k, v in f.items() if k not in des) + 0.3 * len(sel)
random.seed(int(sys.argv[5]) if len(sys.argv) > 5 else 1)
cur = []; c = dist(cur); best = (c, list(cur))
for it in range(IT):
    T0 = 2.0 * (1 - it / IT) + 0.05
    n = list(cur); m = random.random()
    if (m < 0.4 or not n) and len(n) < MAXN: n.append(random.randrange(len(D)))
    elif m < 0.7 and n: n.pop(random.randrange(len(n)))
    elif n: n[random.randrange(len(n))] = random.randrange(len(D))
    nc = dist(n)
    if nc <= c or random.random() < math.exp((c - nc) / T0):
        cur, c = n, nc
        if c < best[0]: best = (c, list(cur))
print('pred', best[0], file=sys.stderr)
print(json.dumps([rows[i]['inj'] for i in best[1]]))
