"""loop.py ROUNDS [start.json]: closed loop. Each round: table.py singles on the current base
(measured fq deltas), anneal subsets of rows (ADD at most per round) scored by hsim inv on the BASE's
real history with f = basefq + sum deltas (additive model; P tied to f where measured P==f), then
measure the top-K predictions for real and keep the best measured (inv, then count)."""
import json, os, sys, random, math, subprocess
ROOT = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, ROOT + r'\tools\wip\mc\s18')
import hsim
import ext, table
D = table.D
ADD = int(os.environ.get('ADD', '4')); TOPK = int(os.environ.get('TOPK', '6')); IT = int(os.environ.get('IT', '20000'))
rounds = int(sys.argv[1])
cur = [tuple(x) for x in json.load(open(sys.argv[2]))] if len(sys.argv) > 2 else []
def tab(base, tag):
    out = os.path.join(D, 'tab_%s.json' % tag)
    subprocess.run([sys.executable, os.path.join(HERE, 'table2.py'), out, os.path.join(D, 'base_%s.json' % tag)],
                   capture_output=True, text=True) if json.dump(base, open(os.path.join(D, 'base_%s.json' % tag), 'w')) is None else None
    return json.load(open(out))
for rnd in range(rounds):
    T = tab(cur, 'r%d' % rnd)
    R, keys = hsim.load(os.path.join(D, 'slot_base'))
    f0, P0 = hsim.measured(keys); f0.update(hsim.armf(os.path.join(D, 'slot_base')))
    tie = {b for b in f0 if P0.get(b) == f0[b] and f0[b] > 0}
    base_inv = T['baseinv']
    rows = [r for r in T['rows'] if not r['miss'] and r['d']]
    Dl = [{int(k): v for k, v in r['d'].items()} for r in rows]
    cache = {}
    def val(sel):
        key = tuple(sorted(sel))
        if key in cache: return cache[key]
        f = dict(f0)
        for i in sel:
            for k, v in Dl[i].items():
                if k in f: f[k] = max(0, f[k] + v)
        P = dict(P0)
        for b in tie: P[b] = f[b]
        x = hsim.inv(hsim.sim(R, f, P)) + 0.2 * len(sel)
        cache[key] = x; return x
    h0 = val([]); print("round", rnd, "base", cur, "inv", base_inv, "hsim", h0, "rows", len(rows), flush=True)
    random.seed(rnd)
    for restart in range(3):
        s = []; c = val(s)
        for it in range(IT):
            t0 = 1.5 * (1 - it / IT) + 0.05
            n = list(s); m = random.random()
            if (m < 0.4 or not n) and len(n) < ADD: n.append(random.randrange(len(Dl)))
            elif m < 0.7 and n: n.pop(random.randrange(len(n)))
            elif n: n[random.randrange(len(n))] = random.randrange(len(Dl))
            x = val(n)
            if x <= c or random.random() < math.exp((c - x) / t0): s, c = n, x
    top = sorted(cache.items(), key=lambda kv: kv[1])[:TOPK]
    best = None
    for k, pred in top:
        inj = cur + [tuple(rows[i]['inj']) for i in k]
        r = table.meas(inj, 'cand')
        if r is None: continue
        print('  pred %.1f meas inv %d' % (pred, r['inv']), [rows[i]['inj'] for i in k], flush=True)
        if best is None or (r['inv'], len(inj)) < best[0]: best = ((r['inv'], len(inj)), inj, r)
    if best is None or best[0][0] >= base_inv:
        print('no measured improvement', flush=True); break
    cur = best[1]
    print('ACCEPT inv', best[0][0], best[2]['order'], flush=True)
    json.dump(cur, open(os.path.join(HERE, 'best.json'), 'w'))
    if best[0][0] == 0: print('INV0'); break
