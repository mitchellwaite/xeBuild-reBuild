"""sa.py SEED N TAG : hill-climb lv genomes by es (event score vs match) + W*ev score. env G start genome, W."""
import sys, os, json, random
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import es
import lv as gen
seed, N, P = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
rng = random.Random(seed); log = open(os.path.join(D, 'sa_%s.jsonl' % P), 'a'); W = float(os.environ.get('W', '1'))
def cost(r): return 1e9 if r is None else r['es'] + W * r['score']
best = json.loads(os.environ.get('G', '{"E": []}'))
for k in ('t48', 'ex1', 'ex2'):
    if best.get(k): best[k] = tuple(best[k])
br = es.run(gen.make(best), P); bc = cost(br); print('start', bc, br, flush=True)
for it in range(N):
    g = gen.mut(best, rng) if rng.random() < .8 else gen.rand(rng)
    try: t = gen.make(g)
    except AssertionError: continue
    r = es.run(t, P); c = cost(r)
    if r: log.write(json.dumps({'g': g, 'score': r['score'], 'es': r['es'], 'per': r['per']}) + '\n'); log.flush()
    if c <= bc: best, bc = g, c; print(it, c, r['score'], r['es'], r['per'], g, flush=True)
