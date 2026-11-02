"""sa3.py SEED SECONDS TAG: hill-climb s51 lv levers on c_r10.c (s53 base). cost = es2 + W*ev. env G start genome, W, BASEF."""
import sys, os, json, random, time
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D); sys.path.insert(0, os.path.join(D, '..', 's51'))
import es2, lv
lv.BASE = open(os.path.join(D, os.environ.get('BASEF', 'c_r10.c'))).read()
seed, T, P = int(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
rng = random.Random(seed); log = open(os.path.join(D, 'sa_%s.jsonl' % P), 'a'); W = float(os.environ.get('W', '1'))
def cost(r): return 1e9 if r is None else r['es2'] + W * r['score']
best = json.loads(os.environ.get('G', '{"E": []}'))
for k in ('t48', 'ex1', 'ex2'):
    if best.get(k): best[k] = tuple(best[k])
br = es2.run(lv.make(best), P); bc = cost(br); print('start', bc, br, flush=True)
t0 = time.time(); it = 0
while time.time() - t0 < T:
    it += 1
    g = lv.mut(best, rng) if rng.random() < .8 else lv.rand(rng)
    try: t = lv.make(g)
    except AssertionError: continue
    r = es2.run(t, P); c = cost(r)
    if r: log.write(json.dumps({'g': g, 'score': r['score'], 'es': r['es'], 'es2': r['es2'], 'per2': r['per2']}, default=list) + '\n'); log.flush()
    if c <= bc: best, bc = g, c; print(it, c, r['score'], r['es'], r['es2'], r['per2'], json.dumps(g, default=list), flush=True)
print('done', it, bc, json.dumps(best, default=list))
