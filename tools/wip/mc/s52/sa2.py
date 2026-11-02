"""sa2.py SEED SECONDS TAG: hill-climb s51 lv levers on top of the s52 fake-label construct (lp4 9,21,0,tail,D,A).
cost = es + W*ev. env G start genome (json), W, BASEV (sp,k1,k2,where,d,hdr)."""
import sys, os, json, random, time
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D); sys.path.insert(0, os.path.join(D, '..', 's51'))
import es, lv, lp4
a = os.environ.get('BASEV', '9,21,0,tail,2,A').split(',')
lv.BASE = lp4.mk(int(a[0]), int(a[1]), int(a[2]), a[3], int(a[4]), a[5])
seed, T, P = int(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
rng = random.Random(seed); log = open(os.path.join(D, 'sa_%s.jsonl' % P), 'a'); W = float(os.environ.get('W', '1'))
def cost(r): return 1e9 if r is None else r['es'] + W * r['score']
best = json.loads(os.environ.get('G', '{"E": []}'))
for k in ('t48', 'ex1', 'ex2'):
    if best.get(k): best[k] = tuple(best[k])
br = es.run(lv.make(best), P); bc = cost(br); print('start', bc, br, flush=True)
t0 = time.time(); it = 0
while time.time() - t0 < T:
    it += 1
    g = lv.mut(best, rng) if rng.random() < .8 else lv.rand(rng)
    try: t = lv.make(g)
    except AssertionError: continue
    r = es.run(t, P); c = cost(r)
    if r: log.write(json.dumps({'g': g, 'base': a, 'score': r['score'], 'es': r['es'], 'per': r['per']}, default=list) + '\n'); log.flush()
    if c <= bc: best, bc = g, c; print(it, c, r['score'], r['es'], r['per'], json.dumps(g, default=list), flush=True)
print('done', it, bc, json.dumps(best, default=list))
