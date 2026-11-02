"""sa.py SEED N TAGPFX : random+mutation search over gen genomes; logs jsonl to s50/sa_TAG.jsonl"""
import sys, os, json, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lv as gen, h
seed, N, P = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
rng = random.Random(seed); log = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sa_%s.jsonl' % P), 'a')
W = float(os.environ.get('W', '3'))
def cost(r): return 1e9 if r is None else r['score'] * W + r['r3s'] * 2
best = json.loads(os.environ['G']) if 'G' in os.environ else {'ji0': False, 'E': []}; br = h.run(gen.make(best), P); bc = cost(br)
for it in range(N):
    g = gen.mut(best, rng) if rng.random() < .7 else gen.rand(rng)
    try: t = gen.make(g)
    except AssertionError: continue
    r = h.run(t, P); c = cost(r)
    if r: log.write(json.dumps({'g': g, 'score': r['score'], 'r3s': r['r3s'], 'r3': r['r3']}) + '\n'); log.flush()
    if c <= bc: best, bc = g, c; print(it, c, r['score'], r['r3s'], g, flush=True)
