"""search.py SEED GENS [init.json]: local search over designs on real compiles.
design = {rok:[..], L:{loopsite:[..]}, F:[[vocsite,[..]]], rx, t48}; score = fncmp + 3*inv."""
import sys, json, random, m, ev, des, voc, loopsites
from multiprocessing import Pool
G = json.load(open('g7b.json'))
MC = voc.MCLABS
FS = ['c1>', 'c2>', 'c3>', 'c8>', 'c9>', 'c11>', 'h4>', 'h5>', 's4>', 's5>', 'p0>', 'p1>', 'i0>', 'eerase<', 'eerase>', 'einv>', 'enet<']
LSITES = list(loopsites.LS)
def text(d):
    des.s0 = voc.make(G + [tuple(x) for x in d['F']], dupl=True)
    t = des.build(rok=','.join(d['rok']), rx=d['rx'], t48=d['t48'])
    for s, tg in d['L'].items():
        if tg: t = loopsites.add(t, s, tg)
    return t
def job(a):
    tag, d = a
    try: r = m.meas(text(d), tag, fncmp=True)
    except Exception as e: return d, None, None
    if 'err' in r: return d, None, None
    inv = ev.score_order(r['order'].split()[1:])[0]
    return d, 10 * inv + r['fncmp'] // 20, (inv, r['fncmp'], r['order'])
def mut(d, R):
    d = json.loads(json.dumps(d))
    k = R.random()
    if k < 0.3:
        x = R.choice(MC)
        if x in d['rok']: d['rok'].remove(x)
        else: d['rok'].insert(R.randrange(len(d['rok']) + 1), x)
    elif k < 0.5:
        s = R.choice(LSITES); tg = d['L'].get(s, [])
        x = R.choice(MC)
        tg = [y for y in tg if y != x] if x in tg else tg + [x]
        d['L'][s] = tg
    elif k < 0.8:
        s = R.choice(FS); ok = voc.targets_for(s)
        cur = [e for e in d['F'] if e[0] == s]
        if cur and R.random() < 0.5: d['F'].remove(cur[0])
        else:
            if cur: d['F'].remove(cur[0])
            d['F'].append([s, R.sample(ok, R.choice([1, 1, 2, 3]))])
    elif k < 0.9: d['rx'] = not d['rx']
    else: d['t48'] = not d['t48']
    return d
if __name__ == '__main__':
    seed, gens = int(sys.argv[1]), int(sys.argv[2]); R = random.Random(seed)
    cur = json.load(open(sys.argv[3])) if len(sys.argv) > 3 else {'rok': [], 'L': {}, 'F': [], 'rx': False, 't48': False}
    pool = Pool(4)
    _, cs, cinfo = job(('q%d_b' % seed, cur)); print('start', cs, cinfo[:2], flush=True)
    best = (cs, cur, cinfo)
    for g in range(gens):
        J = [('q%d_%d' % (seed, i), mut(mut(cur, R), R) if R.random() < 0.3 else mut(cur, R)) for i in range(8)]
        res = [x for x in pool.map(job, J) if x[1] is not None]
        res.sort(key=lambda x: x[1])
        if res and res[0][1] <= cs:
            cur, cs, cinfo = res[0]
            if cs < best[0]: best = (cs, cur, cinfo); json.dump(best, open('best_q%d.json' % seed, 'w'))
        print(g, 'cur', cs, cinfo[:2], 'best', best[0], flush=True)
    print('BEST', best[0], best[2][:2], best[2][2]); print(json.dumps(best[1]))
