# climb.py singles|greedy|pairs|sa SEED : search over gen.py edits
import sys, json, random, math, os
from multiprocessing.pool import ThreadPool
import gen
T = [i for i in gen.SL if any(s in gen.BASE[i] for s in ('client_usage', 'ERROR', 'superseded', 'already been set', 'info dump', 'patch file set'))] + ['rok', 'fail']
ALL = [tuple(e) for e in gen.all_singles(set(T))]
POOL = ThreadPool(int(os.environ.get("NJ","4")))
def ev(es): return gen.evaluate(list(es))
def cost(r): return r[0] * 100 + r[1]
mode = sys.argv[1]
out = open('climb_%s.log' % '_'.join(sys.argv[1:]), 'a')
def log(*a):
    s = ' '.join(map(str, a)); print(s, flush=True); out.write(s + '\n'); out.flush()
if mode == 'singles':
    res = POOL.map(lambda e: (ev([e]), e), ALL)
    res.sort(key=lambda x: cost(x[0]))
    json.dump([[list(r), list(e)] for r, e in res], open('singles.json', 'w'))
    for r, e in res[:60]: log(r, e)
elif mode == 'greedy':
    S = json.load(open(os.environ.get('SJ','singles.json')))
    cand = [tuple(e) for r, e in S if r[0] < 9999][:int(sys.argv[2])]
    cur = []; cr = ev(cur)
    while True:
        rs = POOL.map(lambda e: (ev(cur + [e]), e), [e for e in cand if e not in cur])
        rs.sort(key=lambda x: cost(x[0]))
        if not rs or cost(rs[0][0]) >= cost(cr): break
        cr, e = rs[0]; cur.append(e); log('greedy', cr, cur)
    json.dump(cur, open('greedy.json', 'w')); log('final', cr, cur)
elif mode == 'pairs':
    S = json.load(open(os.environ.get('SJ','singles.json')))
    base = [tuple(e) for e in json.load(open(sys.argv[3]))] if len(sys.argv) > 3 else []
    cand = [tuple(e) for r, e in S if r[0] < 9999][:int(sys.argv[2])]
    pr = [(a, b) for i, a in enumerate(cand) for b in cand[i+1:]]
    rs = POOL.map(lambda p: (ev(base + list(p)), p), pr)
    rs.sort(key=lambda x: cost(x[0]))
    for r, p in rs[:40]: log(r, p)
elif mode == 'sa':
    random.seed(int(sys.argv[2])); n = int(sys.argv[3])
    S = json.load(open(os.environ.get('SJ','singles.json')))
    cand = [tuple(e) for r, e in S if r[0] < 9999][:int(sys.argv[4])]
    cur = [tuple(e) for e in json.load(open(sys.argv[5]))] if len(sys.argv) > 5 else []
    cr = ev(cur); best = (cr, list(cur)); t = 150.0
    for it in range(n):
        new = list(cur)
        if new and random.random() < 0.35: new.pop(random.randrange(len(new)))
        else:
            e = random.choice(cand)
            if e in new: continue
            new.append(e)
        r = ev(new)
        if r[0] >= 9999: continue
        d = cost(r) - cost(cr)
        if d <= 0 or random.random() < math.exp(-d / t): cur, cr = new, r
        if cost(r) < cost(best[0]): best = (r, list(new)); log('best', it, r, new)
        t = max(20, t * 0.99)
    log('final', best)
elif mode == 'bsingles':
    base = [tuple(e) for e in json.load(open(sys.argv[2]))]
    res = POOL.map(lambda e: (ev(base + [e]), e), [e for e in ALL if e not in base])
    res.sort(key=lambda x: cost(x[0]))
    json.dump([[list(r), list(e)] for r, e in res], open('bsingles.json', 'w'))
    for r, e in res[:80]: log(r, e)
